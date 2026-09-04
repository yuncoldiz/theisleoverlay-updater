with open(r'D:\Apps\TheIsleVn-BanhMi\resources\app.asar', 'rb') as f:
    data = f.read()

target1 = b'"version": "1.0.3"'
target2 = b'"version":"1.0.3"'

print('target1 count:', data.count(target1))
print('target2 count:', data.count(target2))
