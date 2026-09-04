import os
import json
import shutil
import sys
from pathlib import Path

def on_rm_error(func, path, exc_info):
    import stat
    os.chmod(path, stat.S_IWRITE)
    func(path)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    src_dir = Path("src_extracted")
    original_backup = Path("resources/app_original")
    if not original_backup.exists():
        print("Error: resources/app_original does not exist!")
        return

    src_dir.mkdir(parents=True, exist_ok=True)

    # 1. Reset dist/assets/index-CealnApy.js, electron/ and package.json to pristine state
    print("Resetting key files to pristine...")
    
    # Reset index-CealnApy.js
    orig_js = original_backup / "dist" / "assets" / "index-CealnApy.js"
    dest_js = src_dir / "dist" / "assets" / "index-CealnApy.js"
    dest_js.parent.mkdir(parents=True, exist_ok=True)
    if dest_js.exists():
        dest_js.unlink()
    shutil.copyfile(orig_js, dest_js)

    # Reset electron/ folder
    orig_elec = original_backup / "electron"
    dest_elec = src_dir / "electron"
    if dest_elec.exists():
        shutil.rmtree(dest_elec, onerror=on_rm_error)
    shutil.copytree(orig_elec, dest_elec)

    # Reset package.json
    orig_pkg = original_backup / "package.json"
    dest_pkg = src_dir / "package.json"
    if dest_pkg.exists():
        dest_pkg.unlink()
    shutil.copyfile(orig_pkg, dest_pkg)

    # 2. Extract index-hNLmMOku.css from logs as the custom CSS baseline
    print("Extracting custom baseline index-hNLmMOku.css from logs...")
    logs_path_1f = r"C:\Users\YunColdiz\.gemini\antigravity-ide\brain\1f487fe6-742b-4d06-ac8a-75dcccd22e6b\.system_generated\logs\transcript_full.jsonl"
    dest_css = src_dir / "dist" / "assets" / "index-hNLmMOku.css"
    dest_css.parent.mkdir(parents=True, exist_ok=True)

    extracted = False
    with open(logs_path_1f, 'r', encoding='utf-8') as f:
        for line in f:
            obj = json.loads(line)
            if obj.get('type') == 'VIEW_FILE':
                content = obj.get('content', '')
                if 'index-hNLmMOku.css' in content and 'File Path:' in content:
                    lines = content.split('\n')
                    file_lines = []
                    for l in lines:
                        if ': ' in l:
                            parts = l.split(': ', 1)
                            if parts[0].strip().isdigit():
                                file_lines.append(parts[1].rstrip('\r\n'))
                    if file_lines:
                        with open(dest_css, 'w', encoding='utf-8', newline='\n') as wf:
                            wf.write('\n'.join(file_lines))
                        print(f"Extracted custom index-hNLmMOku.css baseline from Step {obj.get('step_index')}")
                        extracted = True
                        break
    if not extracted:
        print("Error: Could not extract index-hNLmMOku.css from logs!")
        return

    # 3. Gather all edits to replay (up to 1f487fe6 session inclusive, excluding ffdb02a0)
    convs = [
        {"cid": "60c081d5-877a-4a2b-a414-33a8ed7686f4", "min_step": 0},
        {"cid": "75cd1c35-9edf-4218-a2ef-7643d3e040ba", "min_step": 0},
        {"cid": "2f642991-f3a4-4d36-9f0d-cbcfc7e19dd9", "min_step": 0},
        {"cid": "c4649b00-7b12-40c2-8b17-4c383a510090", "min_step": 0},
        {"cid": "2a216334-e37d-4a2d-888c-187755911090", "min_step": 0},
        {"cid": "7107f83d-e13b-4de1-8cf1-743638fbf01c", "min_step": 0},
        {"cid": "1f487fe6-742b-4d06-ac8a-75dcccd22e6b", "min_step": 0}
    ]

    brain_dir = r"C:\Users\YunColdiz\.gemini\antigravity-ide\brain"
    all_edits = []

    for item in convs:
        cid = item["cid"]
        min_step = item["min_step"]
        log_path = os.path.join(brain_dir, cid, ".system_generated", "logs", "transcript_full.jsonl")
        if not os.path.exists(log_path):
            print(f"Warning: Log not found for {cid}")
            continue

        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                obj = json.loads(line)
                if obj.get('source') == 'MODEL' and 'tool_calls' in obj:
                    step_idx = obj.get('step_index')
                    if step_idx < min_step:
                        continue
                    for tc in obj['tool_calls']:
                        name = tc.get('name')
                        if name in ['write_to_file', 'replace_file_content', 'multi_replace_file_content']:
                            args = tc.get('args', {})
                            if isinstance(args, str):
                                try: args = json.loads(args)
                                except: pass
                            target = args.get('TargetFile', '')
                            
                            target_file = None
                            if 'index-CealnApy.js' in target:
                                target_file = "src_extracted/dist/assets/index-CealnApy.js"
                            elif 'index-hNLmMOku.css' in target:
                                # ONLY replay CSS edits from 1f487fe6
                                if cid in ["1f487fe6-742b-4d06-ac8a-75dcccd22e6b"]:
                                    target_file = "src_extracted/dist/assets/index-hNLmMOku.css"
                            elif 'main.cjs' in target:
                                target_file = "src_extracted/electron/main.cjs"
                            elif 'preload.cjs' in target:
                                target_file = "src_extracted/electron/preload.cjs"
                            elif 'package.json' in target:
                                target_file = "src_extracted/package.json"

                            if target_file:
                                all_edits.append({
                                    'cid': cid,
                                    'step': step_idx,
                                    'tool': name,
                                    'target': target_file,
                                    'args': args
                                })

    print(f"Found {len(all_edits)} edits to replay.")

    for edit in all_edits:
        cid = edit['cid']
        step = edit['step']
        tool = edit['tool']
        target = edit['target']
        args = edit['args']
        print(f"Replaying [{cid}] Step {step}: {tool} on {target}")

        filepath = Path(target)
        if tool == 'write_to_file':
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as wf:
                wf.write(args.get('CodeContent', ''))
        elif tool == 'replace_file_content':
            target_content = args.get('TargetContent', '')
            replacement_content = args.get('ReplacementContent', '')
            
            # Clean line endings to ensure perfect matching
            target_content = target_content.replace('\r\n', '\n').strip()
            replacement_content = replacement_content.replace('\r\n', '\n')
            
            with open(filepath, 'r', encoding='utf-8') as rf:
                content = rf.read().replace('\r\n', '\n')
                
            if target_content in content:
                content = content.replace(target_content, replacement_content, 1)
                with open(filepath, 'w', encoding='utf-8', newline='\n') as wf:
                    wf.write(content)
            else:
                # Retry with relaxed strip matching
                clean_content = content.strip()
                if target_content in clean_content:
                    clean_content = clean_content.replace(target_content, replacement_content, 1)
                    with open(filepath, 'w', encoding='utf-8', newline='\n') as wf:
                        wf.write(clean_content)
                else:
                    print(f"Error: Target content not found in {target} (Step {step})!")
        elif tool == 'multi_replace_file_content':
            with open(filepath, 'r', encoding='utf-8') as rf:
                content = rf.read().replace('\r\n', '\n')
            chunks = args.get('ReplacementChunks', [])
            for chunk in chunks:
                target_content = chunk.get('TargetContent', '').replace('\r\n', '\n').strip()
                replacement_content = chunk.get('ReplacementContent', '').replace('\r\n', '\n')
                if target_content in content:
                    content = content.replace(target_content, replacement_content, 1)
                else:
                    clean_content = content.strip()
                    if target_content in clean_content:
                        content = clean_content.replace(target_content, replacement_content, 1)
                    else:
                        print(f"Error in multi-chunk: Target content not found in {target} (Step {step})!")
            with open(filepath, 'w', encoding='utf-8', newline='\n') as wf:
                wf.write(content)

    # 4. Copy the cropped QR image file to assets
    src_qr = os.path.expandvars('%USERPROFILE%/.gemini/antigravity-ide/brain/1f487fe6-742b-4d06-ac8a-75dcccd22e6b/.user_uploaded/media_1787390997333.png')
    dest_qr = Path("src_extracted/dist/assets/donate_qr.png")
    if os.path.exists(src_qr):
        print(f"Copying QR code image from {src_qr} to {dest_qr}...")
        dest_qr.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_qr, dest_qr)
        print("QR image copied successfully!")
    else:
        print(f"Error: Source QR image not found at {src_qr}")

    print("Workspace recovery completed successfully to 4:30 PM state!")

if __name__ == "__main__":
    main()
