import requests
from bs4 import BeautifulSoup
from goose3 import Goose

def get_blogs(tag):  
    link = "https://medium.com/tag/" + tag
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')
    date = soup.select("div>span>a>p")
    title = soup.select("div>h2")
    link = soup.find_all('a',{"aria-label" :"Post Preview Title"})
    name = soup.select("span>div>a>p")
    blogs = []
    for d, n, t, l in zip(date, name, title, link):
        blogs.append({
            'name' : n.text,
            'link' : "https://medium.com" + l.get('href'),
            'title' : t.text,
            'date': d.text[1:]
        })
    return blogs

def related_tags(tag):
    link = "https://medium.com/tag/" + tag
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')
    related_tags = []
    link = soup.select('#root > div > div.l.c > div > div > div.dk.dl.c.dm.h.k.j.i.bl.dn.do.dp > div > div > div > div.l.gz > div.eh.l > div.ie.gi.l > div > div.o.gk.iu > div')
    for l in link:
        related_tags.append({
            'name' : l.select('div')[0].text,
            'link' : "https://medium.com" + l.select('a')[0].get('href')
        })
    return related_tags

def crawl_blog(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')
    rel_tag = soup.select("ul>li>a")
    clap = ""
    claps = soup.select_one("p>button")
    if claps is not None:
        clap = claps.text
    response = ""
    responses = soup.select_one("button>div>div>p>span")
    if responses is not None:
        response = responses.text
    print(clap, response)
    rel = []
    for r in rel_tag:
        if "https://" in r.text:
            continue
        rel.append(r.text)
    return {
        'num_claps' : clap,
        'num_responses' : response,
        'related_tags' : rel,
    }

def article_text(link):
    g = Goose()
    article = g.extract(url=link)
    g.close()
    print(article.cleaned_text)
    return article.cleaned_text