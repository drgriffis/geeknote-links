import re

tmpFile = 'edump.tmp'
f = open(tmpFile, 'r')
lines = f.readlines()
f.close()

printing = False
for l in lines:
    if not printing:
        if re.match('-* CONTENT -*', l) != None:
            printing = True
    else:
        print l.strip('\r\n')
