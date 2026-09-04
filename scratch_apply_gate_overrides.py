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

    # Correct target with unescaped double quotes exactly matching the file content
    target1 = 'y.jsxs("div",{className:"gate",children:[y.jsxs("svg",{className:"gateMark",viewBox:"0 0 24 24",width:"48",height:"48\",\"aria-hidden\":\"true\",children:[y.jsx("path",{d:\"M12 2 21 7v10l-9 5-9-5V7l9-5Z\",fill:\"none\",stroke:\"currentColor\",strokeWidth:\"1.4\",strokeLinejoin:\"round\"}),y.jsx("path",{d:\"M12 7 16 9.5v5L12 17l-4-2.5v-5L12 7Z\",fill:\"currentColor\",opacity:\"0.9\"})]})],'
    target1_clean = 'y.jsxs("div",{className:"gate",children:[y.jsxs("svg",{className:"gateMark",viewBox:"0 0 24 24",width:"48",height:"48\",\"aria-hidden\":\"true\",children:[y.jsx("path",{d:\"M12 2 21 7v10l-9 5-9-5V7l9-5Z\",fill:\"none\",stroke:\"currentColor\",strokeWidth:\"1.4\",strokeLinejoin:\"round\"}),y.jsx("path",{d:\"M12 7 16 9.5v5L12 17l-4-2.5v-5L12 7Z\",fill:\"currentColor\",opacity:\"0.9\"})]})],'

    # Let's define the exact target string from the file
    exact_target = 'y.jsxs("div",{className:"gate",children:[y.jsxs("svg",{className:"gateMark",viewBox:"0 0 24 24",width:"48",height:"48\",\"aria-hidden\":\"true\",children:[y.jsx("path",{d:\"M12 2 21 7v10l-9 5-9-5V7l9-5Z\",fill:\"none\",stroke:\"currentColor\",strokeWidth:\"1.4\",strokeLinejoin:\"round\"}),y.jsx("path",{d:\"M12 7 16 9.5v5L12 17l-4-2.5v-5L12 7Z\",fill:\"currentColor\",opacity:\"0.9\"})]})],'
    exact_target = exact_target.replace('\\"', '"') # Convert escaped quotes to normal quotes

    replacement1 = 'y.jsxs("div",{className:"gate",children:[y.jsx("img",{className:"gateMarkLogo",src:"./assets/logo.jpg",style:{width:"120px",height:"120px",borderRadius:"50%",border:"2px solid var(--phos)",marginBottom:"16px",boxShadow:"0 0 15px var(--phos)"}}),'

    if exact_target in content:
        content = content.replace(exact_target, replacement1)
        print("Successfully replaced Gate Logo with img logo!")
        with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
    else:
        # Check substring match
        sub = 'y.jsxs("div",{className:"gate",children:[y.jsxs("svg",{className:"gateMark"'
        idx = content.find(sub)
        if idx != -1:
            end_idx = content.find(')],', idx) + 3
            target_found = content[idx:end_idx]
            content = content.replace(target_found, replacement1)
            print("Successfully replaced Gate Logo with img logo (dynamic)!")
            with open(js_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
        else:
            print("Failed to find Gate Logo target in JS bundle!")

if __name__ == '__main__':
    main()
