import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    data = f.read()

idx = data.find('Z==="account"')
if idx != -1:
    print("Found Z===account at", idx)
    print(data[idx:idx+2500])
else:
    print("account not found")
