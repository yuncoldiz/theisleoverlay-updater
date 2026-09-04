import os
import json
import datetime

def list_conversations():
    brain_path = os.path.expandvars('%USERPROFILE%/.gemini/antigravity-ide/brain')
    if not os.path.exists(brain_path):
        print("Brain path not found")
        return
        
    conversations = []
    for folder in os.listdir(brain_path):
        log_file = os.path.join(brain_path, folder, '.system_generated', 'logs', 'transcript.jsonl')
        if os.path.exists(log_file):
            mtime = os.path.getmtime(log_file)
            mtime_dt = datetime.datetime.fromtimestamp(mtime)
            
            # Read first line to get start date if possible
            start_time = "Unknown"
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if '"type":"USER_INPUT"' in line:
                            data = json.loads(line)
                            # Maybe we can find the date in some other way, but mtime is good
                            break
            except:
                pass
                
            conversations.append({
                'folder': folder,
                'mtime': mtime_dt
            })
            
    conversations.sort(key=lambda x: x['mtime'])
    for c in conversations:
        print(f"Folder: {c['folder']} | Last Modified: {c['mtime'].strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    list_conversations()
