#!/usr/bin/env python
# Hardcoding by Jimmyromanticdevil aka rahmat ramadhan iryanto
# romanticdevil.jimmy@gmail.com
# you can distribution anything do you want
# https://jimmyromanticdevil.wordpress.com
# webcrawler(romanticdevil-crawler.py)
import urllib2
import BeautifulSoup 
import sys
import urllib
from BeautifulSoup import BeautifulSoup as ziachow
import urlparse
from urllib2 import urlopen
from urllib import urlretrieve
import os
import os.path
import re
import random
out_folder = ""
user_agent  = ['Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/20100207 Ubuntu/9.04 (jaunty) Namoroka/3.6.2pre',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
        'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
            'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.6)',
            'Microsoft Internet Explorer/4.0b1 (Windows 95)',
            'Opera/8.00 (Windows NT 5.1; U; en)',
        'amaya/9.51 libwww/5.4.0',
        'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
        'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
        'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]'
        ]
 
 
#fungsi untuk mendownload page
def download(url):
    url_request = urllib.urlopen(url)
    try:
        localFile = open(url.split('/')[-1], 'w')
        localFile.write(url_request.read())
        url_request.close()
        localFile.close()
    except:
        pass
 
#fungsi untuk mendownload image
def download_image(url):
    soup = ziachow(urlopen(url))
    parsed = list(urlparse.urlparse(url))
 
    for image in soup.findAll("img"):
        try:
            filename = image["src"].split("/")[-1]
            if os.path.isfile(filename) or os.path.isfile(parsed[2]):
                break
            else:
                print "Image Download: %(src)s" % image
                parsed[2] = image["src"]
                outpath = os.path.join(out_folder, filename)
                if image["src"].lower().startswith("http"):
                    urlretrieve(image["src"], outpath)
                else:
                    urlretrieve(urlparse.urlunparse(parsed), outpath)
 
        except:
            break
                 
 
#fungsi untuk mendownload css                
def download_css(url):
    
    try:
        soup = ziachow(urlopen(url))
        parsed = list(urlparse.urlparse(url))
        for image in soup.findAll("link"):
            try:
                filename = image["href"].split("/")[-1]
                parsed[2] = image["href"]
                if os.path.isfile(filename) or os.path.isfile(parsed[2]):
                    break
                else:   
                    print "Css Download: %(href)s" % image
                    outpath = os.path.join(out_folder, filename)
                    if image["href"].lower().startswith("http"):
                        urlretrieve(image["href"], outpath)
                    else:
                        urlretrieve(urlparse.urlunparse(parsed), outpath)
            except:
                break
    except:
        pass        
 
 
#fungsi untuk mendownload js
def download_js(url):
    try:
        soup = ziachow(urlopen(url))
        parsed = list(urlparse.urlparse(url))
        for image in soup.findAll("script"):
            try: 
                filename = image["src"].split("/")[-1]
                if os.path.isfile(filename) or os.path.isfile(parsed[2]):
                   break
                else:   
                   print "Javascript/Jquery Download: %(src)s" % image
                   parsed[2] = image["src"]
                   outpath = os.path.join(out_folder, filename)
                   if image["src"].lower().startswith("src"):
                      urlretrieve(image["src"], outpath)
                   else:
                      urlretrieve(urlparse.urlunparse(parsed), outpath) 
            except:
                break
 
      except:
         pass        
 
def main(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', random.choice(user_agent))]
    page = opener.open(url)
    htmlcode_page = page.read() 
    dump_isihtml = BeautifulSoup.BeautifulSoup(htmlcode_page)
    print dump_isihtml.title.string 
    Links = dump_isihtml.findAll("a", {"href": True}) 
    leng = len(Links)   
    count = 0   
    while count < leng:
        try:   
            url_match = re.findall("((http\://|https\://|ftp\://)|(www.))+(([a-zA-Z0-9\.-]+\.[a-zA-Z]{2,4})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9%:/-_\?\.'~]*)?", Links[count]["href"])
      
            if Links[count]["href"] == "#" or Links[count]["href"] == "" or os.path.isfile(Links[count]["href"]):
                print 'page available or got filter'
                count +=1
            elif url_match:
                print 'Fetch page %s'%Links[count]["href"]
                download(Links[count]["href"])
                download_css(Links[count]["href"])
                download_image(Links[count]["href"])
                download_js(Links[count]["href"])
                count += 1  
         
            else:
                print 'Fetch page %s'%Links[count]["href"]
                download(url+'/'+Links[count]["href"])
                download_css(url+'/'+Links[count]["href"])
                download_image(url+'/'+Links[count]["href"])
                download_js(url+'/'+Links[count]["href"])
                count += 1 
        except:
            count +=1
             
if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            main(sys.argv[1])
        except Exception,err:
            print err
        else:
            print 'usage: %s http://server.com/ ' % os.path.basename(sys.argv[0])
