import asar
from pathlib import Path
import json

archive = asar.AsarArchive(Path('resources/app.asar'), 'r')
# asar python module: let's see how it stores files in archive
# Let's inspect archive._asar_io or archive header
with open('resources/app.asar', 'rb') as f:
    import struct
    f.seek(4)
    header_size = struct.unpack('<I', f.read(4))[0]
    header_raw_size = struct.unpack('<I', f.read(4))[0]
    f.seek(16)
    header_json = f.read(header_raw_size).decode('utf-8')
    header = json.loads(header_json)

def find_in_tree(files, path=''):
    for name, info in files.items():
        curr = f"{path}/{name}" if path else name
        if 'files' in info:
            find_in_tree(info['files'], curr)
        else:
            if 'index' in name or 'backup' in name:
                print(f"File: {curr}, size: {info.get('size')}, offset: {info.get('offset')}")

find_in_tree(header.get('files', {}))
