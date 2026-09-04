import asar
import sys
import shutil
import os
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
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main():
    src_dir = Path("src_extracted")
    dest_asar = Path("resources/app.asar")
    dest_unpacked = Path("resources/app.asar.unpacked")
    
    print("Cleaning up old unpacked resources...")
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
        
    print(f"Packing '{src_dir}' into '{dest_asar}'...")
    with CustomAsarArchive(dest_asar, "w") as archive:
        archive.pack(src_dir)
        
    print("Successfully repacked app.asar!")

if __name__ == "__main__":
    main()
