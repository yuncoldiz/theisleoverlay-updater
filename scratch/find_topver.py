import glob

for f in glob.glob('src_extracted/**', recursive=True):
    try:
        with open(f, 'rb') as fp:
            c = fp.read()
            if b'topVer' in c:
                print('topVer found in:', f)
    except:
        pass
