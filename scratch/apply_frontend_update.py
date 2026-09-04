import sys

with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Target 1: State declarations and record functions in Tj
target1 = '[rKey,setRKey]=B.useState((n==null?void 0:n.radarKey)??"Ctrl+M"),[rRec,setRRec]=B.useState(!1),'
repl1 = '[rKey,setRKey]=B.useState((n==null?void 0:n.radarKey)??"Ctrl+M"),[rRec,setRRec]=B.useState(!1),[rlKey,setRlKey]=B.useState((n==null?void 0:n.reloadKey)??"Ctrl+Shift+R"),[rlRec,setRlRec]=B.useState(!1),[rsKey,setRsKey]=B.useState((n==null?void 0:n.resetLayoutKey)??"Ctrl+Shift+L"),[rsRec,setRsRec]=B.useState(!1),'

# Target 2: Record functions in Tj
target2 = 'async function recordRKey(){setRRec(!0);const le=await window.isleOverlay.recordMapKey();setRRec(!1),le&&setRKey(le)}'
repl2 = 'async function recordRKey(){setRRec(!0);const le=await window.isleOverlay.recordMapKey();setRRec(!1),le&&setRKey(le)}async function recordRlKey(){setRlRec(!0);const le=await window.isleOverlay.recordReloadKey();setRlRec(!1),le&&setRlKey(le)}async function recordRsKey(){setRsRec(!0);const le=await window.isleOverlay.recordResetLayoutKey();setRsRec(!1),le&&setRsKey(le)}'

# Target 3: Widgets tab reset layout quick button
target3 = 'y.jsx("div",{className:"secLabel",children:"phím tắt bản đồ radar"}),y.jsx("div",{className:"hint",children:"hiển thị hoặc ẩn Bản đồ radar bằng phím tắt"}),y.jsxs("div",{className:"hint",style:{marginTop:6},children:["phím hiện tại · ",rKey]}),y.jsxs("div",{className:"featRow",style:{flexWrap:"wrap"},children:[["Ctrl+M","F9","Ctrl+F9"].map(le=>y.jsx("button",{className:`chip ${rKey===le?"on":""}`,onClick:()=>{setRKey(le),window.isleOverlay.setSettings({radarKey:le})},children:le},le)),y.jsx("button",{className:`chip ${rRec?"on":""}`,onClick:recordRKey,children:rRec?"BẤM PHÍM BẤT KỲ…":"+ TÙY CHỌN"})]})'
repl3 = target3 + ',y.jsx("div",{className:"secLabel",children:"khôi phục vị trí mặc định"}),y.jsx("div",{className:"hint",children:"nếu widget bị kéo ra ngoài màn hình, bấm nút dưới để đặt lại vị trí chuẩn"}),y.jsx("div",{className:"featRow",children:y.jsx("button",{className:"chip",style:{background:"rgba(56,189,248,0.15)",borderColor:"#38bdf8",color:"#38bdf8"},onClick:()=>window.isleOverlay.resetLayout(),children:"↺ ĐẶT LẠI VỊ TRÍ MẶC ĐỊNH (RESET LAYOUT)"})})'

# Target 4: Controls tab hotkey settings for reload and reset layout
target4 = 'y.jsx("div",{className:"secLabel",children:"phím tắt dashboard"}),y.jsx("div",{className:"hint",children:"hiển thị hoặc ẩn bảng Dashboard cùng lúc với con trỏ chuột bằng 1 phím"}),y.jsxs("div",{className:"hint",style:{marginTop:6},children:["phím hiện tại · ",N]}),y.jsxs("div",{className:"featRow",style:{flexWrap:"wrap"},children:[j.map(le=>y.jsx("button",{className:`chip ${N===le?"on":""}`,onClick:()=>{X(le),window.isleOverlay.setSettings({dashKey:le})},children:le},le)),y.jsx("button",{className:`chip ${W?"on":""}`,onClick:ee,children:W?"BẤM PHÍM BẤT KỲ…":"+ TÙY CHỌN"})]})'
repl4 = target4 + ',y.jsx("div",{className:"secLabel",children:"phím tắt reload giao diện"}),y.jsx("div",{className:"hint",children:"tải lại giao diện overlay và kết nối lại máy chủ khi bị lag hoặc đứng hình"}),y.jsxs("div",{className:"hint",style:{marginTop:6},children:["phím hiện tại · ",rlKey]}),y.jsxs("div",{className:"featRow",style:{flexWrap:"wrap"},children:[["Ctrl+Shift+R","F9","Ctrl+F9"].map(le=>y.jsx("button",{className:`chip ${rlKey===le?"on":""}`,onClick:()=>{setRlKey(le),window.isleOverlay.setSettings({reloadKey:le})},children:le},le)),y.jsx("button",{className:`chip ${rlRec?"on":""}`,onClick:recordRlKey,children:rlRec?"BẤM PHÍM BẤT KỲ…":"+ TÙY CHỌN"}),y.jsx("button",{className:"chip",style:{background:"rgba(74,222,128,0.15)",borderColor:"#4ade80",color:"#4ade80"},onClick:()=>window.isleOverlay.reloadApp(),children:"⚡ TẢI LẠI NGAY"})]}),y.jsx("div",{className:"secLabel",children:"phím tắt khôi phục vị trí hud"}),y.jsx("div",{className:"hint",children:"khôi phục vị trí các widget và radar về mặc định khi bị kéo lệch khỏi màn hình"}),y.jsxs("div",{className:"hint",style:{marginTop:6},children:["phím hiện tại · ",rsKey]}),y.jsxs("div",{className:"featRow",style:{flexWrap:"wrap"},children:[["Ctrl+Shift+L","F10","Ctrl+F10"].map(le=>y.jsx("button",{className:`chip ${rsKey===le?"on":""}`,onClick:()=>{setRsKey(le),window.isleOverlay.setSettings({resetLayoutKey:le})},children:le},le)),y.jsx("button",{className:`chip ${rsRec?"on":""}`,onClick:recordRsKey,children:rsRec?"BẤM PHÍM BẤT KỲ…":"+ TÙY CHỌN"}),y.jsx("button",{className:"chip",style:{background:"rgba(56,189,248,0.15)",borderColor:"#38bdf8",color:"#38bdf8"},onClick:()=>window.isleOverlay.resetLayout(),children:"↺ ĐẶT LẠI VỊ TRÍ"})]})'

# Target 5: Guide tab
target5 = 'y.jsx("div",{style:{marginLeft:"12px"},children:"• Khi bật Chế độ Streamer, hãy thêm nguồn \'Window Capture\' trong OBS và chọn cửa sổ \'TheIsleVN - YTB BanhMi\' để quay màn hình."})]})'
repl5 = target5 + ',y.jsxs("div",{children:[y.jsx("strong",{style:{color:"var(--phos)"},children:"5. Tải lại giao diện (Reload):"}),y.jsx("div",{style:{marginLeft:"12px"},children:"• Mặc định là Ctrl+Shift+R (hoặc F9). Giúp làm mới toàn bộ HUD và kết nối lại máy chủ khi bị lag hoặc đơ."})]}),y.jsxs("div",{children:[y.jsx("strong",{style:{color:"var(--phos)"},children:"6. Đặt lại vị trí mặc định (Reset Layout):"}),y.jsx("div",{style:{marginLeft:"12px"},children:"• Mặc định là Ctrl+Shift+L (hoặc F10). Đưa toàn bộ các widget và radar về vị trí chuẩn ban đầu."})]})'

# Target 6: Hy fallback to defaultPos if layout is reset
target6 = 'B.useEffect(()=>{i&&typeof i.x=="number"&&s(i)},[i==null?void 0:i.x,i==null?void 0:i.y])'
repl6 = 'B.useEffect(()=>{s(i&&typeof i.x=="number"?i:e)},[i==null?void 0:i.x,i==null?void 0:i.y])'

for i, (t, r) in enumerate([(target1, repl1), (target2, repl2), (target3, repl3), (target4, repl4), (target5, repl5), (target6, repl6)], 1):
    cnt = code.count(t)
    if cnt != 1:
        print(f"Error: target {i} matched {cnt} times!")
        sys.exit(1)
    code = code.replace(t, r, 1)

with open('src_extracted/dist/assets/index-CealnApy.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated src_extracted/dist/assets/index-CealnApy.js!")
