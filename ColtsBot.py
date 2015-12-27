from bs4 import BeautifulSoup
import urllib.request as url
import re

TAG_RE = re.compile(r'<[^>]+>')
html_str = "<!DOCTYPE html><html><head><title>Page Title</title></head><body>"
run = True

#get news from colts
def getNewsLinks():
    global html_str
    news_links = []
    news_titles = []
    summaries =[]
    html_str +="<h1>Colt Daily News</h1>"
    website = "http://www.colts.com/news/all-news.html"
    htmlfile = url.urlopen(website)
    soup = BeautifulSoup(htmlfile)
    for link in soup.findAll('a', href=True):
        if('news/article' in link.get('href')):
            page = "http://www.colts.com" + link.get('href')
            news_links.append(page)
            news_titles.append(link.get('title'))
        
    #remove duplicate links
    news_links = remove_duplicates(news_links)
    news_titles = remove_duplicates(news_titles)

    for x in range(len(news_titles)):
        html_str += format_data(news_titles[x] , news_links[x])
        
    
            
#get videos from colts
def getVideoLinks():
    global html_str
    items = []
    video_links = []
    mp4_links = []
    titles = []
    html_str +="<h1>Colt Daily Videos</h1>"
    website = "http://www.colts.com/videos/all-videos.html"
    htmlfile = url.urlopen(website)
    soup = BeautifulSoup(htmlfile)

    for link in soup.findAll('a', href=True):
        if('/videos/videos' in link.get('href')):
            video_links.append(link.get('href'))
    
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
        title = remove_tags(str(titles[x]))
        html_str += format_data(title , mp4_links[x])


#Format data
def format_data(title, link):
    hyperlink_format = '<a href=%s>%s</a><br>' %(link, title)
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
    getVideoLinks()
    getNewsLinks()
    html_str += "</body></html>"
    HTML_file=open("Colts.html", "w")
    HTML_file.write(html_str)
    HTML_file.close()
    run = False
