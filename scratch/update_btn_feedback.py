with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    c = f.read()

target = 'onClick:()=>{window.isleOverlay.checkManualUpdate&&window.isleOverlay.checkManualUpdate()},children:"🔄 KIỂM TRA CẬP NHẬT"'
print("Target found:", target in c)

replacement = 'onClick:async(e)=>{const b=e.currentTarget;const old=b.textContent;b.textContent="⏳ ĐANG KIỂM TRA...";try{window.isleOverlay.checkManualUpdate&&await window.isleOverlay.checkManualUpdate()}catch{}finally{setTimeout(()=>{b.textContent=old},1800)}},children:"🔄 KIỂM TRA CẬP NHẬT"'

c = c.replace(target, replacement)
with open('src_extracted/dist/assets/index-CealnApy.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('Successfully upgraded check update button feedback!')
