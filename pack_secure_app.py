import asar
import sys
import shutil
import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path

class CustomAsarArchive(asar.AsarArchive):
    def _pack(self, path: Path, src: Path, unpack: str):
        path_in = path.relative_to(src)
        posix_path = path_in.as_posix()
        
        # Check if the path belongs to native modules that must be unpacked
        should_unpack = False
        for prefix in ["node_modules/koffi", "node_modules/uiohook-napi", "node_modules/@koromix"]:
            if posix_path == prefix or posix_path.startswith(prefix + "/"):
                should_unpack = True
                break
        
        if path.is_symlink():
            node = self._search_node_from_path(path_in)
            node.set_link(path.resolve().relative_to(src))
            if node.link.parts[0] == "..":
                raise ValueError(f"{path_in}: file \"{node.link}\" links out of the package")
        elif path.is_dir():
            node = self._search_node_from_path(path_in)
            node.set_dir(unpacked=should_unpack)
            for child in path.iterdir():
                self._pack(child, src, unpack)
        else:
            if not hasattr(self, '_file_count'):
                self._file_count = 0
            self._file_count += 1
            if self._file_count % 500 == 0:
                print(f"Packed {self._file_count} files...")
                sys.stdout.flush()
            self.pack_file(
                path_in,
                path,
                should_unpack=should_unpack,
            )

def on_rm_error(func, path, exc_info):
    # Deal with read-only files on Windows during cleanup
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def check_global_node():
    try:
        # Run node -v to see if it is available globally
        result = subprocess.run(["node", "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print(f"Found global Node.js: {result.stdout.strip()}")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def setup_portable_node(scratch_dir: Path):
    node_dir = scratch_dir / "node-portable"
    node_exe = node_dir / "node.exe"
    
    if node_exe.exists():
        print(f"Portable Node.js found at: {node_exe}")
        return node_dir
        
    scratch_dir.mkdir(parents=True, exist_ok=True)
    zip_path = scratch_dir / "node-portable.zip"
    
    # Node.js portable zip URL
    node_url = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-win-x64.zip"
    print(f"Downloading portable Node.js from {node_url}...")
    sys.stdout.flush()
    
    # Download helper with progress indicator
    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = min(100, readsofar * 100 // totalsize)
            sys.stdout.write(f"\rDownloading: {percent}% ({readsofar // (1024*1024)}MB / {totalsize // (1024*1024)}MB)")
            sys.stdout.flush()
        else:
            sys.stdout.write(f"\rDownloading: {readsofar // 1024} KB")
            sys.stdout.flush()
            
    urllib.request.urlretrieve(node_url, zip_path, reporthook)
    print("\nExtracting Node.js zip...")
    sys.stdout.flush()
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(scratch_dir)
        
    # Rename extracted directory to node-portable
    extracted_dir = scratch_dir / "node-v20.11.0-win-x64"
    if extracted_dir.exists():
        if node_dir.exists():
            shutil.rmtree(node_dir, onerror=on_rm_error)
        extracted_dir.rename(node_dir)
        
    # Clean up zip file
    if zip_path.exists():
        zip_path.unlink()
        
    print(f"Portable Node.js successfully set up at: {node_dir}")
    return node_dir

def run_obfuscator(node_dir, file_path: Path):
    print(f"Obfuscating: {file_path.relative_to(Path('.'))}")
    sys.stdout.flush()
    
    # Arguments for javascript-obfuscator
    # We use safe settings to protect strings while maintaining performance
    obfuscator_args = [
        "--compact", "true",
        "--string-array", "true",
        "--string-array-encoding", "base64",
        "--rename-globals", "false",
        "--control-flow-flattening", "false",
        "--dead-code-injection", "false"
    ]
    
    # Prepare environment variables
    env = os.environ.copy()
    if node_dir is not None:
        node_dir_abs = str(node_dir.resolve())
        env["PATH"] = node_dir_abs + os.pathsep + env.get("PATH", "")
        
    if node_dir is None:
        # Use global node and npx
        cmd = ["npx", "javascript-obfuscator", str(file_path)] + obfuscator_args + ["--output", str(file_path)]
    else:
        # Use portable node and npx-cli.js
        node_exe = str(node_dir / "node.exe")
        npx_cli = str(node_dir / "node_modules" / "npm" / "bin" / "npx-cli.js")
        cmd = [node_exe, npx_cli, "javascript-obfuscator", str(file_path)] + obfuscator_args + ["--output", str(file_path)]
        
    # Run the command
    result = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Error obfuscating {file_path}:")
        print(result.stderr)
        raise RuntimeError(f"Obfuscation failed for {file_path}")

def main():
    src_dir = Path("src_extracted")
    temp_src_dir = Path("src_extracted_secured")
    dest_asar = Path("resources/app.asar")
    dest_unpacked = Path("resources/app.asar.unpacked")
    scratch_dir = Path("scratch")
    
    print("--- STEP 1: Setting up Node.js for Obfuscation ---")
    node_dir = None
    if not check_global_node():
        print("Global Node.js not detected. Setting up portable Node.js...")
        node_dir = setup_portable_node(scratch_dir)
    else:
        print("Using global Node.js.")
        
    print("\n--- STEP 2: Preparing Temporary Directory ---")
    if temp_src_dir.exists():
        print("Cleaning up old temporary directory...")
        shutil.rmtree(temp_src_dir, onerror=on_rm_error)
        
    print(f"Creating a temporary copy of '{src_dir}' as '{temp_src_dir}'...")
    shutil.copytree(
        src_dir,
        temp_src_dir,
        ignore=shutil.ignore_patterns("*.bak*", "*.backup*", "*.log", "*~")
    )
    
    print("\n--- STEP 3: Obfuscating JS Source Files ---")
    # Identify files to obfuscate
    files_to_obfuscate = [
        temp_src_dir / "electron" / "main.cjs",
        temp_src_dir / "electron" / "preload.cjs",
        temp_src_dir / "electron" / "native-windows.cjs"
    ]
    
    # Glob for index-*.js files in dist/assets
    assets_dir = temp_src_dir / "dist" / "assets"
    if assets_dir.exists():
        for js_file in assets_dir.glob("index-*.js"):
            files_to_obfuscate.append(js_file)
            
    # Run obfuscator on each file
    for f in files_to_obfuscate:
        if f.exists():
            run_obfuscator(node_dir, f)
        else:
            print(f"Warning: File not found for obfuscation: {f}")
            
    print("\n--- STEP 4: Cleaning up Old App ASAR ---")
    if dest_unpacked.exists():
        try:
            shutil.rmtree(dest_unpacked, onerror=on_rm_error)
        except Exception as e:
            print(f"Warning: failed to fully clean resources/app.asar.unpacked: {e}")
            
    # Back up the original app.asar if not already backed up
    backup_asar = Path("resources/app.asar.bak")
    if not backup_asar.exists() and dest_asar.exists():
        print("Creating backup of original app.asar at resources/app.asar.bak...")
        shutil.copyfile(dest_asar, backup_asar)
        
    print(f"\n--- STEP 5: Packing Obfuscated '{temp_src_dir}' into '{dest_asar}' ---")
    with CustomAsarArchive(dest_asar, "w") as archive:
        archive.pack(temp_src_dir)
        
    print("\n--- STEP 6: Cleaning up Temporary Directory ---")
    if temp_src_dir.exists():
        shutil.rmtree(temp_src_dir, onerror=on_rm_error)
        
    print("\n--- SUCCESS: App packed and secured successfully! ---")

if __name__ == "__main__":
    main()
