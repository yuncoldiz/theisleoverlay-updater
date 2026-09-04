import os
import json
import shutil
import sys
import datetime
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

    # Reset workspace to pristine baseline
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

    # Extract index-hNLmMOku.css baseline
    print("Extracting custom baseline index-hNLmMOku.css from logs...")
    logs_path_1f = r"C:\Users\YunColdiz\.gemini\antigravity-ide\brain\1f487fe6-742b-4d06-ac8a-75dcccd22e6b\.system_generated\logs\transcript_full.jsonl"
    dest_css = src_dir / "dist" / "assets" / "index-hNLmMOku.css"
    dest_css.parent.mkdir(parents=True, exist_ok=True)

    extracted = False
    if os.path.exists(logs_path_1f):
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

    # Find all conversations modified between Aug 20 and Aug 22 18:00 (6:00 PM)
    brain_dir = r"C:\Users\YunColdiz\.gemini\antigravity-ide\brain"
    convs = []
    
    cut_off_time = datetime.datetime(2026, 8, 22, 18, 0, 0)
    start_filter_time = datetime.datetime(2026, 8, 20, 0, 0, 0)

    for folder in os.listdir(brain_dir):
        log_file = os.path.join(brain_dir, folder, '.system_generated', 'logs', 'transcript.jsonl')
        if os.path.exists(log_file):
            mtime = os.path.getmtime(log_file)
            mtime_dt = datetime.datetime.fromtimestamp(mtime)
            if start_filter_time <= mtime_dt <= cut_off_time:
                convs.append({
                    'cid': folder,
                    'mtime': mtime_dt
                })

    # Sort conversations by last modification time (oldest to newest)
    convs.sort(key=lambda x: x['mtime'])
    print("Conversations to replay in chronological order:")
    for c in convs:
        print(f"  - {c['cid']} (Modified: {c['mtime'].strftime('%Y-%m-%d %H:%M:%S')})")

    all_edits = []
    for item in convs:
        cid = item["cid"]
        log_path_full = os.path.join(brain_dir, cid, ".system_generated", "logs", "transcript_full.jsonl")
        log_path_short = os.path.join(brain_dir, cid, ".system_generated", "logs", "transcript.jsonl")
        
        log_path = log_path_full if os.path.exists(log_path_full) else log_path_short
        if not os.path.exists(log_path):
            continue

        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                obj = json.loads(line)
                if obj.get('source') == 'MODEL' and 'tool_calls' in obj:
                    step_idx = obj.get('step_index')
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
                                # Only replay CSS edits in session 1f487
                                if cid == "1f487fe6-742b-4d06-ac8a-75dcccd22e6b":
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

    print(f"Gathered {len(all_edits)} edits to replay.")

    # Replay edits
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

    # Copy the correct QR code image
    src_qr = os.path.expandvars('%USERPROFILE%/.gemini/antigravity-ide/brain/1f487fe6-742b-4d06-ac8a-75dcccd22e6b/.user_uploaded/media_1787390997333.png')
    dest_qr = Path("src_extracted/dist/assets/donate_qr.png")
    if os.path.exists(src_qr):
        print(f"Copying QR code image from {src_qr} to {dest_qr}...")
        dest_qr.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_qr, dest_qr)
        print("QR image copied successfully!")
    else:
        print(f"Error: Source QR image not found at {src_qr}")

    print("Checking bracket balance on resulting index-CealnApy.js...")
    validate_js_bracket(dest_js)

def validate_js_bracket(filepath):
    if not filepath.exists():
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    stack = []
    state_stack = ['NORMAL']
    pairs = {')': '(', ']': '[', '}': '{'}
    i = 0
    n = len(code)
    has_error = False

    while i < n:
        state = state_stack[-1]
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if i + 1 < n and code[i] == '/' and code[i+1] == '/':
                i += 2
                while i < n and code[i] != '\n':
                    i += 1
                continue
            if i + 1 < n and code[i] == '/' and code[i+1] == '*':
                i += 2
                while i + 1 < n and not (code[i] == '*' and code[i+1] == '/'):
                    i += 1
                i += 2
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[i] in ['\'', '\"']:
                quote = code[i]
                i += 1
                while i < n and code[i] != quote:
                    if code[i] == '\\':
                        i += 2
                    else:
                        i += 1
                i += 1
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[i] == '`':
                state_stack.append('TEMPLATE_LITERAL')
                i += 1
                continue
        elif state == 'TEMPLATE_LITERAL':
            if code[i] == '`':
                state_stack.pop()
                i += 1
                continue
            elif code[i] == '\\':
                i += 2
                continue
            elif i + 1 < n and code[i] == '$' and code[i+1] == '{':
                state_stack.append('TEMPLATE_EXPR')
                stack.append(('${', i))
                i += 2
                continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            if code[i] == '/':
                prev_idx = i - 1
                while prev_idx >= 0 and code[prev_idx].isspace():
                    prev_idx -= 1
                if prev_idx >= 0 and code[prev_idx] not in ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','_',')',']','}']:
                    i += 1
                    while i < n and code[i] != '/':
                        if code[i] == '\\':
                            i += 2
                        else:
                            i += 1
                    i += 1
                    continue
        if state in ['NORMAL', 'TEMPLATE_EXPR']:
            char = code[i]
            if char in '([{':
                stack.append((char, i))
            elif char in ')]}':
                if not stack:
                    print(f"Unmatched closing char {char} at pos {i}: {repr(code[max(0, i-40):i+40])}")
                    has_error = True
                    break
                else:
                    top_char, top_pos = stack.pop()
                    if char == '}':
                        if top_char == '${':
                            if state_stack[-1] == 'TEMPLATE_EXPR':
                                state_stack.pop()
                        elif top_char != '{':
                            print(f"Mismatch: opened {top_char} at {top_pos} but closed {char} at {i}")
                            has_error = True
                            break
                    else:
                        if top_char != pairs[char]:
                            print(f"Mismatch: opened {top_char} at {top_pos} but closed {char} at {i}")
                            has_error = True
                            break
        i += 1
    if stack and not has_error:
        print("Unclosed brackets at end:", len(stack))
    elif not has_error:
        print("All brackets matched in JS!")

if __name__ == '__main__':
    main()
