import os

exe_path = 'TheIsleVn-BanhMi.exe'

old_str = 'TheIsleVN-Gacha-HUD'.encode('utf-16le')
new_str = 'TheIsleVn-BanhMi-VN'.encode('utf-16le')

assert len(old_str) == len(new_str), f"Lengths must match! {len(old_str)} vs {len(new_str)}"

with open(exe_path, 'rb') as f:
    content = f.read()

count = content.count(old_str)
print(f"Found {count} occurrences of {old_str}")
assert count == 3, f"Expected 3 occurrences, got {count}"

new_content = content.replace(old_str, new_str)
assert len(new_content) == len(content), "Binary size must remain identical!"

with open(exe_path, 'wb') as f:
    f.write(new_content)

print("Successfully updated TheIsleVn-BanhMi.exe!")
