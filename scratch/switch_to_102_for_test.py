import os
import json

asar_path = r'D:\Apps\TheIsleVn-BanhMi\resources\app.asar'

with open(asar_path, 'rb') as f:
    data = f.read()

target = b'"version": "1.0.3"'
replacement = b'"version": "1.0.2"'

count = data.count(target)
print(f'Found {count} occurrences of {target}')

assert count > 0, 'No target version found in asar'

new_data = data.replace(target, replacement)
assert len(new_data) == len(data), 'Asar size changed!'

with open(asar_path, 'wb') as f:
    f.write(new_data)

print('Successfully patched installed app.asar to version 1.0.2!')

# Also ensure dismissedUpdateVersion is null in settings.json
settings_path = os.path.expandvars(r'%APPDATA%\theisleinformation-bybanhmibietchoi\theisleinformation-bybanhmibietchoi.settings.json')
if os.path.exists(settings_path):
    with open(settings_path, 'r', encoding='utf-8') as f:
        settings = json.load(f)
    settings['dismissedUpdateVersion'] = None
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2)
    print('Reset dismissedUpdateVersion to null in settings.json!')
