import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    text = f.read()

for tab in ['controls', 'appearance', 'account', 'guide']:
    pos = text.find(f'Z==="{tab}"')
    if pos != -1:
        print(f"=== TAB {tab.upper()} ===")
        print(text[pos:pos+800])
        print('-'*50)
