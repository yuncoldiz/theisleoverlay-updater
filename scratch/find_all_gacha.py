import os

targets = ['gacha', 'Gacha', 'GACHA']
found = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or 'scratch' in root:
        continue
    for f in files:
        if f.endswith('.exe') or f.endswith('.dll') or f.endswith('.bin') or f.endswith('.pak') or f.endswith('.dat'):
            continue
        p = os.path.join(root, f)
        try:
            with open(p, 'rb') as fp:
                c = fp.read()
                for t in targets:
                    if t.encode('utf-8') in c or t.encode('utf-16le') in c:
                        found.append((p, t))
                        break
        except Exception as e:
            pass

for f, t in found:
    print(f"Match: {f} (found {t})")
