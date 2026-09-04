with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    content = f.read()

count_before = content.count('1.0.0')
print('Count of 1.0.0 before:', count_before)

# Replace the 3 exact occurrences of 1.0.0
content_new = content.replace('children:["v","1.0.0"]', 'children:["v","1.0.1"]')
content_new = content_new.replace('v","1.0.0"]', 'v","1.0.1"]')

count_after = content_new.count('1.0.0')
print('Count of 1.0.0 after:', count_after)
print('Count of 1.0.1 after:', content_new.count('1.0.1'))

with open('src_extracted/dist/assets/index-CealnApy.js', 'w', encoding='utf-8') as f:
    f.write(content_new)

print('Updated index-CealnApy.js successfully!')
