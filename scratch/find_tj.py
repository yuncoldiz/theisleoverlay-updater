import sys

with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('function Tj(')
print('idx:', idx)
if idx != -1:
    with open('scratch/tj_code.txt', 'w', encoding='utf-8') as out:
        out.write(c[idx:idx+15000])
    print("Wrote 15000 chars to scratch/tj_code.txt")
