from bs4 import BeautifulSoup
import urllib.request as url
import re

TAG_RE = re.compile(r'<[^>]+>')
items = []
video_links = []
mp4_links = []
titles = []
html_str = "<!DOCTYPE html><html><head><title>Page Title</title></head><body><h1>Colt Daily Videos</h1>"
run = True

#get videos from colts
def getLinks():
    global html_str
    global run
    global items
    global video_links
    global mp4_links
    global titles
    website = "http://www.colts.com/videos/all-videos.html"
    htmlfile = url.urlopen(website)
    soup = BeautifulSoup(htmlfile)

    for link in soup.findAll('a', href=True):
        items.append(link.get('href'))
    
    for x in items:
        if('/videos/videos' in x):
            video_links.append(x)

    for x in video_links:
        website = "http://www.colts.com/" + x
        htmlfile = url.urlopen(website)
        soup = BeautifulSoup(htmlfile)
        for link in soup.findAll('meta'):
            if('mp4' in link.get('content')):
                mp4_links.append(link.get('content'))
                
        for title in soup.findAll('title'):
            titles.append(title)

    #remove duplicate links
    mp4_links = remove_duplicates(mp4_links)
    titles = remove_duplicates(titles)
           
    for x in range(len(titles)):
        #print(titles[x], mp4_links[x])
        title = remove_tags(str(titles[x]))
        html_str += format_data(title , mp4_links[x])
        run = False
    html_str += "</body></html>"
    HTML_file=open("Colts.html", "w")
    HTML_file.write(html_str)
    HTML_file.close()


#Format data
def format_data(title, mp4_link):
    hyperlink_format = '<a href=%s>%s</a><br>' %(mp4_link, title)
    return hyperlink_format

#remove dubplicates in list
def remove_duplicates(objects):
    last = objects[-1]
    for i in range(len(objects)-2, -1, -1):
       if last == objects[i]:
           del objects[i]
       else:
           last = objects[i]
    return objects

    
#remove title tags
def remove_tags(text):
    return TAG_RE.sub('', text)

while(run):
    getLinks()
