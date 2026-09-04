with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    c = f.read()

target1 = 'children:["v","1.0.2"]'
target2 = 'children:["OVERLAY · v","1.0.2"]'
target3 = 'children:["TheIsleVN - YTB BanhMi · v","1.0.2"]'

print("target1 in c:", target1 in c)
print("target2 in c:", target2 in c)
print("target3 in c:", target3 in c)

c = c.replace(target1, 'children:["v","1.0.3"]')
c = c.replace(target2, 'children:["OVERLAY · v","1.0.3"]')
c = c.replace(target3, 'children:["TheIsleVN - YTB BanhMi · v","1.0.3"]')

with open('src_extracted/dist/assets/index-CealnApy.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('Success! Count of 1.0.3:', c.count('1.0.3'))
print('Remaining 1.0.2:', c.count('1.0.2'))
