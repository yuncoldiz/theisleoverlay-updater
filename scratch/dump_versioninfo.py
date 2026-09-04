with open('TheIsleVn-BanhMi.exe', 'rb') as f:
    data = f.read()

# Let's inspect the exact block around the version info
start = 180193500
end = 180194200
sub = data[start:end]

# Print string table entries
import re
print("Hex dump:")
for i in range(0, len(sub), 32):
    chunk = sub[i:i+32]
    hex_str = ' '.join(f'{b:02x}' for b in chunk)
    ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
    print(f"{start+i:08x}:  {hex_str:<96}  {ascii_str}")
