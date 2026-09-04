with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    c = f.read()

count_before = c.count('1.0.1')
print('Count of 1.0.1 before:', count_before)

c = c.replace('children:["v","1.0.1"]', 'children:["v","1.0.2"]')
c = c.replace('v","1.0.1"]', 'v","1.0.2"]')

count_after = c.count('1.0.2')
print('Count of 1.0.2 after:', count_after)

with open('src_extracted/dist/assets/index-CealnApy.js', 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated index-CealnApy.js successfully!')
