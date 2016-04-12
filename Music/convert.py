import commands

fls = commands.getoutput('ls *.mid').splitlines()
for f in fls:
    newFile = f.split('.')[0] + '.xml'
    cmd = 'mscore %s -o %s'%(f, newFile)
    print cmd
