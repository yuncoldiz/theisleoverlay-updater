with open('src_extracted/dist/assets/index-hNLmMOku.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .secLabel
old_sec = '.secLabel{font-family:var(--mono);font-size:10px;letter-spacing:.1em;color:var(--faint);margin-top:2px}'
new_sec = (
    '.secLabel{font-family:var(--font);font-size:13px;font-weight:700;letter-spacing:.06em;'
    'text-transform:uppercase;color:#7cf2a6;text-shadow:0 0 10px rgba(124,242,166,.35);'
    'margin-top:16px;padding-top:10px;border-top:1px solid rgba(124,242,166,.18);width:100%;'
    'display:flex;align-items:center;gap:8px}'
    '.secLabel:first-of-type{margin-top:0;padding-top:0;border-top:none}'
    '.secLabel::before{content:"";display:inline-block;width:4px;height:13px;background:#7cf2a6;'
    'border-radius:2px;box-shadow:0 0 8px #7cf2a6;flex-shrink:0}'
)
assert old_sec in css, "old_sec not found"
css = css.replace(old_sec, new_sec)

# Replace .hint
old_hint = '.hint{color:var(--faint);font-size:10px}'
new_hint = '.hint{color:#c8e6d2;font-size:11.5px;font-weight:500;line-height:1.5;margin-bottom:2px}'
assert old_hint in css, "old_hint not found"
css = css.replace(old_hint, new_hint)

# Replace .chip and .chip.on
old_chip = '.chip{border:1px solid var(--line);background:transparent;color:var(--muted);font-family:var(--mono);font-size:10px;letter-spacing:.05em;padding:4px 8px;border-radius:999px;cursor:pointer}'
new_chip = (
    '.chip{border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.05);color:#e5f6eb;'
    'font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.05em;padding:5px 11px;'
    'border-radius:999px;cursor:pointer;transition:all .15s ease}'
    '.chip:hover{border-color:#7cf2a6;color:#ffffff;background:rgba(124,242,166,.15);box-shadow:0 0 8px rgba(124,242,166,.25)}'
)
assert old_chip in css, "old_chip not found"
css = css.replace(old_chip, new_chip)

old_chip_on = '.chip.on{border-color:var(--edge);color:var(--phos);background:#e97ca514}'
new_chip_on = '.chip.on{border-color:#7cf2a6;color:#031208;background:#7cf2a6;font-weight:700;box-shadow:0 0 14px rgba(124,242,166,.55)}'
assert old_chip_on in css, "old_chip_on not found"
css = css.replace(old_chip_on, new_chip_on)

# Replace .settingsRailBtn and .settingsRailBtn.on
old_rail = '.settingsRailBtn{text-align:left;border:0;background:transparent;color:var(--muted);font-size:12px;font-weight:600;padding:8px 10px;border-radius:8px;cursor:pointer}'
new_rail = (
    '.settingsRailBtn{text-align:left;border:0;background:transparent;color:#9ab4a2;font-size:12.5px;'
    'font-weight:600;padding:9px 12px;border-radius:8px;cursor:pointer;transition:all .15s ease}'
    '.settingsRailBtn:hover{color:#ffffff;background:rgba(255,255,255,.08)}'
)
assert old_rail in css, "old_rail not found"
css = css.replace(old_rail, new_rail)

old_rail_on = '.settingsRailBtn.on{color:var(--text);background:#e97ca524}'
new_rail_on = '.settingsRailBtn.on{color:#ffffff;background:rgba(124,242,166,.18);border-left:3px solid #7cf2a6;font-weight:700;text-shadow:0 0 8px rgba(124,242,166,.4)}'
assert old_rail_on in css, "old_rail_on not found"
css = css.replace(old_rail_on, new_rail_on)

with open('src_extracted/dist/assets/index-hNLmMOku.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('Successfully upgraded CSS in index-hNLmMOku.css!')
