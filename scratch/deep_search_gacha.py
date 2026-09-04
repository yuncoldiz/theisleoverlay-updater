import os, re

def search_text_files():
    hits = []
    # search src_extracted
    for root, dirs, files in os.walk('src_extracted'):
        if 'node_modules' in root:
            continue
        for f in files:
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    matches = list(re.finditer(r'gacha', content, re.IGNORECASE))
                    if matches:
                        hits.append((p, len(matches), [content[max(0, m.start()-30):min(len(content), m.end()+30)] for m in matches[:5]]))
            except Exception as e:
                pass
    return hits

print("--- TEXT SEARCH IN src_extracted ---")
for p, count, snippets in search_text_files():
    print(f"{p} ({count} occurrences):")
    for s in snippets:
        print("   ...", repr(s), "...")

print("\n--- BINARY SEARCH IN TheIsleVn-BanhMi.exe ---")
with open('TheIsleVn-BanhMi.exe', 'rb') as f:
    exe_data = f.read()

for enc_name, target in [('ascii', b'gacha'), ('utf-16le', 'gacha'.encode('utf-16le'))]:
    matches = [m.start() for m in re.finditer(re.escape(target), exe_data, re.IGNORECASE)]
    print(f"Format {enc_name}: {len(matches)} occurrences at offsets {matches}")
