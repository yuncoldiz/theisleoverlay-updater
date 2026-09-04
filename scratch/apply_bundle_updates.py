import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'src_extracted/dist/assets/index-CealnApy.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update Streaming tab instructions
target_streaming = 'Z==="streaming"&&y.jsxs(y.Fragment,{children:[y.jsx("div",{className:"secLabel",children:"chế độ streamer / obs"}),y.jsx("div",{className:"hint",children:\'Makes this overlay a normal, capturable window so it shows up in OBS. Add a "Window Capture" source and pick "TheIsleVN - YTB BanhMi".\'}),y.jsx("div",{className:"featRow",children:y.jsx("button",{className:`chip ${me?"on":""}`,onClick:()=>{const le=!me;Y(le),window.isleOverlay.setSettings({streamerMode:le})},children:me?"BẬT":"TẮT"})}),y.jsx("div",{className:"hint",style:{marginTop:6},children:`Sử dụng phương thức quay cửa sổ "Windows 10 (1903+)". Nếu nền không tự động trong suốt, vui lòng thêm bộ lọc Chroma/Color key hoặc giảm độ mờ nguồn ghi.`})]})'

replacement_streaming = 'Z==="streaming"&&y.jsxs(y.Fragment,{children:[y.jsx("div",{className:"secLabel",children:"CHẾ ĐỘ STREAMER / OBS"}),y.jsx("div",{className:"hint",children:"Bật chế độ này để Overlay hiện thành cửa sổ cố định, giúp OBS/Streamlabs/Prism dễ dàng nhận diện và khóa khung hình."}),y.jsx("div",{className:"featRow",children:y.jsx("button",{className:`chip ${me?"on":""}`,onClick:()=>{const le=!me;Y(le),window.isleOverlay.setSettings({streamerMode:le})},children:me?"BẬT":"TẮT"})}),y.jsxs("div",{className:"hint",style:{marginTop:8,lineHeight:"1.55",background:"rgba(124,242,166,0.08)",padding:"10px 12px",borderRadius:"8px",border:"1px solid rgba(124,242,166,0.25)"},children:[y.jsx("strong",{style:{color:"#7cf2a6"},children:"💡 HƯỚNG DẪN QUAY BẰNG OBS SIÊU TIỆN LỢI:"}),y.jsx("div",{style:{marginTop:4},children:"1. Bấm BẬT Chế độ Streamer ở trên để cửa sổ hiển thị."}),y.jsx("div",{children:"2. Mở OBS -> Thêm nguồn \'Window Capture (Quay cửa sổ)\' -> Chọn \'TheIsleVN - YTB BanhMi\' (hoặc \'TheIsleVN - Radar Overlay\')."}),y.jsx("div",{style:{color:"#ffcf4a",fontWeight:600,marginTop:3},children:"3. (Quan trọng) Sau khi OBS đã nhận khung hình, hãy bấm TẮT Chế độ Streamer đi! OBS vẫn sẽ quay mượt mà mà bạn không hề bị vướng víu hay che màn hình khi Alt+Tab."})]})]})'

# 2. Update Guide tab Streamer section
target_guide = 'y.jsxs("div",{children:[y.jsx("strong",{style:{color:"var(--phos)"},children:"4. OBS / Chế độ Streamer:"}),y.jsx("div",{style:{marginLeft:"12px"},children:"• Khi bật Chế độ Streamer, hãy thêm nguồn \'Window Capture\' trong OBS và chọn cửa sổ \'TheIsleVN - YTB BanhMi\' để quay màn hình."})]})'

replacement_guide = 'y.jsxs("div",{children:[y.jsx("strong",{style:{color:"var(--phos)"},children:"4. OBS / Chế độ Streamer:"}),y.jsx("div",{style:{marginLeft:"12px",lineHeight:"1.5"},children:"• B1: Bật \'Chế độ Streamer\' trong cài đặt để cửa sổ Overlay cố định hiện diện trên màn hình."}),y.jsx("div",{style:{marginLeft:"12px",lineHeight:"1.5"},children:"• B2: Vào OBS -> Thêm nguồn \'Window Capture\' -> Chọn cửa sổ \'TheIsleVN - YTB BanhMi\' (hoặc \'TheIsleVN - Radar Overlay\')."}),y.jsx("div",{style:{marginLeft:"12px",lineHeight:"1.5",color:"#ffcf4a",fontWeight:600},children:"• B3 (Quan trọng): Sau khi OBS đã nhận và khóa khung hình, hãy TẮT \'Chế độ Streamer\' đi! OBS vẫn sẽ tiếp tục thu hình bình thường mà bạn không hề bị vướng víu khi chơi game."})]})'

# 3. Update Account tab with Manual Check Update button
target_account = 'y.jsx("div",{className:"secLabel",children:"thông tin ứng dụng"}),y.jsxs("div",{className:"hint",children:["TheIsleVN - YTB BanhMi · v","1.0.1"]}),y.jsx("div",{className:"hint",children:"Coded by YTB BanhMi"})'

replacement_account = 'y.jsx("div",{className:"secLabel",children:"thông tin ứng dụng"}),y.jsxs("div",{className:"hint",children:["TheIsleVN - YTB BanhMi · v","1.0.1"]}),y.jsx("div",{className:"hint",children:"Coded by YTB BanhMi"}),y.jsx("button",{className:"tbtn",style:{marginTop:10,background:"rgba(124,242,166,0.18)",border:"1px solid #7cf2a6",color:"#7cf2a6",fontWeight:700,letterSpacing:"0.04em",padding:"8px 14px",boxShadow:"0 0 10px rgba(124,242,166,0.2)"},onClick:()=>{window.isleOverlay.checkManualUpdate&&window.isleOverlay.checkManualUpdate()},children:"🔄 KIỂM TRA CẬP NHẬT"})'

found_streaming = target_streaming in code
found_guide = target_guide in code
found_account = target_account in code

print(f"Target streaming found: {found_streaming}")
print(f"Target guide found: {found_guide}")
print(f"Target account found: {found_account}")

if found_streaming and found_guide and found_account:
    code = code.replace(target_streaming, replacement_streaming, 1)
    code = code.replace(target_guide, replacement_guide, 1)
    code = code.replace(target_account, replacement_account, 1)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Successfully updated index-CealnApy.js!")
else:
    print("ERROR: One or more targets were not matched exactly.")
    sys.exit(1)
