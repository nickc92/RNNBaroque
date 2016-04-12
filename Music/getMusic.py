import cookielib, urllib2, mechanize, zipfile, StringIO

br = mechanize.Browser()
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar(cookiejar)

# Broser options
br.set_handle_equiv( True )
br.set_handle_gzip( True )
br.set_handle_redirect( True )
br.set_handle_referer( True )
br.set_handle_robots( False )

# ??
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 )

br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]

br.open('https://musescore.com/user/login')
for form in br.forms():
    if form.attrs['id'] == 'user-login':
        br.form = form
        break

br['name'] = 'ncholy@gmail.com'
br['pass'] = 'IsqAMx4hqM5k'
res = br.submit()

def getXML(url):
    res = br.open(url)
    fl = res.read()
    stringFl = StringIO.StringIO(fl)
    zf = zipfile.ZipFile(stringFl)
    for fname in zf.namelist():
        if fname.find('lg') >= 0 and fname.find('xml') >= 0:
            print 'extracting', fname
            zf.extract(fname)

for ln in open('urls.txt'):
    if ln.find('href=') >= 0:
        pc = ln.split('href="')[1].split('"')[0].split('/')[-1]
        print pc
        try:
            getXML('https://musescore.com/score/%s/download/mxl'%(pc))
        except Exception, e:
            print e
            
