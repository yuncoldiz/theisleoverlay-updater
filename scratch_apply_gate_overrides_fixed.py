import os
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    js_path = 'src_extracted/dist/assets/index-CealnApy.js'
    if not os.path.exists(js_path):
        print("JS file not found")
        return
        
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace Gate Logo (escaped or unescaped)
    sub = 'y.jsxs("div",{className:"gate",children:[y.jsxs("svg",{className:"gateMark"'
    idx = content.find(sub)
    if idx != -1:
        # Search for the end of the SVG child: )]}),
        end_idx = content.find(')]}),', idx) + 5
        if end_idx != -1 + 5:
            target_found = content[idx:end_idx]
            replacement1 = 'y.jsxs("div",{className:"gate",children:[y.jsx("img",{className:"gateMarkLogo",src:"./assets/logo.jpg",style:{width:"120px",height:"120px",borderRadius:"50%",border:"2px solid var(--phos)",marginBottom:"16px",boxShadow:"0 0 15px var(--phos)"}}),'
            content = content.replace(target_found, replacement1)
            print("Successfully replaced Gate Logo with img logo!")
        else:
            print("Failed to find end of SVG children array!")
    else:
        print("Failed to find Gate Logo start in JS bundle!")

    # 2. Replace Gate text and inject Server API URL input field
    target2 = 'y.jsx("div",{className:"gateTtl",children:"Sign in to TheIsleVn-BanhMiBietChoi"}),y.jsx("div",{className:"gateSub",children:"Log in with Steam to load your dino stats, garage, skins and the live map."}),y.jsxs("button",{className:"steamBtn",onClick:l,'
    
    replacement2 = 'y.jsx("div",{className:"gateTtl",children:"Sign in to TheIsleVn-BanhMiBietChoi"}),y.jsx("div",{className:"gateSub",children:"Log in with Steam to load your dino stats, garage, skins and the live map."}),y.jsxs("div",{style:{marginBottom:"16px",width:"100%"},children:[y.jsx("div",{style:{fontSize:"11px",color:"var(--muted)",marginBottom:"4px",textAlign:"left"},children:"Server API URL:"}),y.jsx("input",{className:"gNameInput interactive-region",style:{width:"100%",boxSizing:"border-box",padding:"8px",background:"#0a0f0d",border:"1px solid var(--line)",borderRadius:"4px",color:"#fff",fontFamily:"monospace"},defaultValue:t?.apiBaseUrl||"https://theisle.gachacity.vn",onChange:ev=>window.isleOverlay.setSettings({apiBaseUrl:ev.target.value})})]}),y.jsxs("button",{className:"steamBtn",onClick:l,'

    if target2 in content:
        content = content.replace(target2, replacement2)
        print("Successfully injected Server API URL input box!")
    else:
        # Check substring match
        sub2 = 'y.jsx("div",{className:"gateTtl",children:"Sign in to TheIsleVn-BanhMiBietChoi"})'
        if sub2 in content:
            idx2 = content.find(sub2)
            end_idx2 = content.find('y.jsxs("button",{className:"steamBtn",onClick:l,', idx2)
            if end_idx2 != -1:
                target2_dyn = content[idx2:end_idx2]
                content = content.replace(target2_dyn, replacement2.replace(',y.jsxs("button",{className:"steamBtn",onClick:l,', ''))
                print("Successfully injected Server API URL input box (dynamic)!")
            else:
                print("Failed to find button end for target 2")
        else:
            print("Failed to find Server API URL target in JS bundle!")

    with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

if __name__ == '__main__':
    main()
