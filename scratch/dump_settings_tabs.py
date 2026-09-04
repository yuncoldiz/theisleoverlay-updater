import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('Z==="widgets"')
if pos != -1:
    print("=== WIDGETS TAB ===")
    print(text[pos:pos+2000])

pos_radar = text.find('Z==="radar"')
if pos_radar != -1:
    print("=== RADAR TAB ===")
    print(text[pos_radar:pos_radar+1500])
