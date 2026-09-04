import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'"streaming"', text):
    p = m.start()
    print("MATCH AT:", p)
    print(text[p-50:p+700])
    print('='*50)
