import re

def check_file(path):
    print("Checking:", path)
    try:
        with open(path, 'rb') as f:
            content = f.read()
            # search for 1.0.0 and 1.0.1
            m1 = len(re.findall(rb'1\.0\.0', content))
            m2 = len(re.findall(rb'1\.0\.1', content))
            print(f"  Count of '1.0.0': {m1}, Count of '1.0.1': {m2}")
            # Search for topVer
            for m in re.finditer(rb'topVer', content):
                s = max(0, m.start() - 20)
                e = min(len(content), m.end() + 50)
                print("  Snippet:", content[s:e])
    except Exception as e:
        print("  Error:", e)

check_file('resources/app.asar')
check_file(r'D:\Apps\TheIsleVn-BanhMi\resources\app.asar')
check_file(r'D:\Apps\TheIsleVn-BanhMi\TheIsleVn-BanhMi\resources\app.asar')
