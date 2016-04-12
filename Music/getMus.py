import commands

for i in range(100):
    cmd = 'wget -O page.html "https://musescore.com/sheetmusic?page=%d&parts=1&text=bwv"; grep span page.html | grep href | grep -i bwv >> urls.txt'%(i)
    print cmd
    commands.getoutput(cmd)
    
