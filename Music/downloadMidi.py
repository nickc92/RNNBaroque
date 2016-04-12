import commands, sys

url = sys.argv[1]
cmd = 'wget -O - ' + url
output = commands.getoutput(cmd)
for ln in output.splitlines():
    refStr = None
    if ln.find('HREF="') >= 0:
        refStr = 'HREF="'
    if ln.find('href="') >= 0:
        refStr = 'href="'
    if refStr != None:
        ref = ln.split(refStr)[1].split('"')[0]
        if ref[-4:].strip() == '.mid':
            theUrl = ref
            if theUrl.find('http') < 0:
                theUrl = 'http://www.jsbach.net/midi/' + ref
            cmd = 'wget ' + theUrl
            
            print commands.getoutput(cmd)
