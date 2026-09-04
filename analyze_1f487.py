import json
import os
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    brain_dir = r'C:\Users\YunColdiz\.gemini\antigravity-ide\brain'
    for folder in os.listdir(brain_dir):
        log_file = os.path.join(brain_dir, folder, '.system_generated', 'logs', 'transcript_full.jsonl')
        if not os.path.exists(log_file):
            log_file = os.path.join(brain_dir, folder, '.system_generated', 'logs', 'transcript.jsonl')
        if not os.path.exists(log_file):
            continue
            
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                if data.get('source') == 'MODEL' and 'tool_calls' in data:
                    for tc in data['tool_calls']:
                        name = tc.get('name')
                        if name in ['write_to_file', 'replace_file_content', 'multi_replace_file_content']:
                            args = tc.get('args', {})
                            if isinstance(args, str):
                                try: args = json.loads(args)
                                except: pass
                            cmd = args.get('CodeContent', '') or args.get('ReplacementContent', '') or ''
                            if 'statsWidgetHorizontal' in cmd:
                                print(f"Conv {folder} | Step {data.get('step_index')}: {name} (contains statsWidgetHorizontal)")

if __name__ == '__main__':
    main()
