import json
import hashlib
import base64
import os
from datetime import datetime
from pathlib import Path

def get_app_version():
    pkg_path = Path("src_extracted/package.json")
    if not pkg_path.exists():
        raise FileNotFoundError("Could not find src_extracted/package.json to read version.")
    with open(pkg_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("version", "1.0.0")

def calculate_sha512_base64(filepath):
    sha512 = hashlib.sha512()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha512.update(chunk)
    return base64.b64encode(sha512.digest()).decode("utf-8")

def main():
    setup_file = Path("TheIsleVn-BanhMi-Setup.exe")
    if not setup_file.exists():
        print(f"Error: Setup file '{setup_file}' not found. Please compile it first.")
        return

    try:
        version = get_app_version()
    except Exception as e:
        print(f"Error reading version: {e}")
        return

    print(f"Reading setup file: {setup_file}...")
    file_size = setup_file.stat().st_size
    
    print("Calculating SHA-512 checksum...")
    sha512_hash = calculate_sha512_base64(setup_file)
    
    # Format release date in ISO UTC format
    release_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    latest_yml_content = f"""version: {version}
files:
  - url: {setup_file.name}
    sha512: {sha512_hash}
    size: {file_size}
path: {setup_file.name}
sha512: {sha512_hash}
releaseDate: '{release_date}'
"""

    output_path = Path("latest.yml")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(latest_yml_content)

    print("\n--- SUCCESS: latest.yml generated successfully! ---")
    print(f"Version: {version}")
    print(f"File Size: {file_size} bytes")
    print(f"SHA-512 (Base64): {sha512_hash}")
    print(f"Release Date: {release_date}")

if __name__ == "__main__":
    main()
