with open('src_extracted/dist/assets/index-CealnApy.js', 'r', encoding='utf-8') as f:
    content = f.read()

count_before = content.count('1.0.3')
print('Count of 1.0.3 before:', count_before)

# Replace the 3 exact occurrences of 1.0.3
content_new = content.replace('children:["v","1.0.3"]', 'children:["v","1.0.4"]')
content_new = content_new.replace('v","1.0.3"]', 'v","1.0.4"]')

count_after = content_new.count('1.0.3')
print('Count of 1.0.3 after:', count_after)
print('Count of 1.0.4 after:', content_new.count('1.0.4'))

with open('src_extracted/dist/assets/index-CealnApy.js', 'w', encoding='utf-8') as f:
    f.write(content_new)

print('Updated index-CealnApy.js successfully!')
