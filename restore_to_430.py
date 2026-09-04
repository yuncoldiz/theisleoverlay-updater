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

    # Create src_extracted if it doesn't exist
    src_dir.mkdir(parents=True, exist_ok=True)

    # 1. Reset dist, electron, and package.json to pristine app_original versions (skip node_modules)
    for name in ["dist", "electron", "package.json"]:
        src_path = src_dir / name
        orig_path = original_backup / name
        if orig_path.exists():
            print(f"Resetting {name} to pristine state...")
            if src_path.exists():
                if src_path.is_dir():
                    shutil.rmtree(src_path, onerror=on_rm_error)
                else:
                    src_path.unlink()
            
            if orig_path.is_dir():
                shutil.copytree(orig_path, src_path)
            else:
                shutil.copyfile(orig_path, src_path)

    # 2. Parse previous conversation transcript logs
    logs_path = r"C:\Users\YunColdiz\.gemini\antigravity-ide\brain\1f487fe6-742b-4d06-ac8a-75dcccd22e6b\.system_generated\logs\transcript_full.jsonl"
    if not os.path.exists(logs_path):
        print(f"Error: Previous logs not found at {logs_path}")
        return

    edits = []
    with open(logs_path, 'r', encoding='utf-8') as f:
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
                        if 'src_extracted' in target or 'pack_app.py' in target:
                            # Convert absolute paths to workspace relative paths
                            rel_target = target.replace("c:\\Users\\YunColdiz\\Desktop\\theisleoverlay-banhmibietchoi\\", "")
                            rel_target = rel_target.replace("C:\\Users\\YunColdiz\\Desktop\\theisleoverlay-banhmibietchoi\\", "")
                            rel_target = rel_target.replace("c:/Users/YunColdiz/Desktop/theisleoverlay-banhmibietchoi/", "")
                            rel_target = rel_target.replace("C:/Users/YunColdiz/Desktop/theisleoverlay-banhmibietchoi/", "")
                            edits.append({
                                'step': step_idx,
                                'tool': name,
                                'target': rel_target,
                                'args': args
                            })

    # Sort edits by step_index
    edits.sort(key=lambda x: x['step'])
    print(f"Found {len(edits)} tool edits in logs. Replaying now...")

    for edit in edits:
        step = edit['step']
        tool = edit['tool']
        target = edit['target']
        args = edit['args']
        print(f"Replaying Step {step}: {tool} on {target}")

        filepath = Path(target)
        if not filepath.exists() and tool != 'write_to_file':
            print(f"Warning: File {target} does not exist for replaying {tool}!")
            continue

        if tool == 'write_to_file':
            # Write file
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as wf:
                wf.write(args.get('CodeContent', ''))
        elif tool == 'replace_file_content':
            target_content = args.get('TargetContent', '')
            replacement_content = args.get('ReplacementContent', '')
            with open(filepath, 'r', encoding='utf-8') as rf:
                content = rf.read()
            if target_content in content:
                new_content = content.replace(target_content, replacement_content, 1)
                with open(filepath, 'w', encoding='utf-8') as wf:
                    wf.write(new_content)
            else:
                print(f"Error at Step {step}: Target content not found in {target}!")
        elif tool == 'multi_replace_file_content':
            with open(filepath, 'r', encoding='utf-8') as rf:
                content = rf.read()
            chunks = args.get('ReplacementChunks', [])
            for chunk in chunks:
                target_content = chunk.get('TargetContent', '')
                replacement_content = chunk.get('ReplacementContent', '')
                if target_content in content:
                    content = content.replace(target_content, replacement_content, 1)
                else:
                    print(f"Error at Step {step} multi-chunk: Target content not found in {target}!")
            with open(filepath, 'w', encoding='utf-8') as wf:
                wf.write(content)

    # 3. Copy the QR code image file
    src_qr = os.path.expandvars('%USERPROFILE%/.gemini/antigravity-ide/brain/1f487fe6-742b-4d06-ac8a-75dcccd22e6b/.user_uploaded/media_1787390997333.png')
    dest_qr = Path("src_extracted/dist/assets/donate_qr.png")
    if os.path.exists(src_qr):
        print(f"Copying QR code image from {src_qr} to {dest_qr}...")
        dest_qr.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_qr, dest_qr)
        print("QR image copied successfully!")
    else:
        print(f"Error: Source QR image not found at {src_qr}")

    print("Successfully restored the workspace to 4:30 PM August 22 state!")

if __name__ == "__main__":
    main()
