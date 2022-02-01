from django.http import JsonResponse
from .models import Tags, Blogs
from django.shortcuts import redirect, render
from .scraping import article_text, get_blogs, related_tags, crawl_blog
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def error_404_view(request, exception):
    return render(request, '404.html')

def index(request):
    return render(request, "scraper/index.html")

def search(request):
    if request.method == "GET":
        return redirect('index')
    else:
        if not request.POST.get("tag"):
            tag_list = ['data science', 'machine learning', 'backend', 'frontend', 'python', 'java']
            return render(request, "scraper/error.html", {'error' : 'Enter a tag', 'tag_list' : tag_list})
        else:
            tag = request.POST.get("tag", None)
            tag = tag.replace(" ", "-")
            tag = tag.lower()
            print(tag)
            tags = related_tags(tag)
            tag_db = Tags(tags=tag)
            tag_db.save()
            get_blog = []
            tags = related_tags(tag)
            i = 0
            while True:
                get_blog = get_blogs(tag)
                tags = related_tags(tag)
                if get_blog and tags:
                    break
                if i == 7:
                    break
                i = i + 1
            if len(get_blog) == 0 and len(tags) == 0:
                tag_list = ['data science', 'machine learning', 'backend', 'frontend', 'python', 'java']
                return render(request, "scraper/error.html", {'error' : 'Invalid tag', 'tag_list' : tag_list})
            if len(get_blog) == 0 or len(tags) == 0:
                return render(request, "scraper/error.html", {'error' : 'Request Timeout'})
            context = {'urls': get_blog, 'tags' : tags}
            return render(request, 'scraper/search.html', context)

def history(request):
    tags = Tags.objects.all().order_by('date').reverse()
    url_paginator = Paginator(tags, 10)
    urls = request.GET.get('page')
    try:
        url_1 = url_paginator.page(urls)
    except PageNotAnInteger:
        url_1 = url_paginator.page(1)
    except EmptyPage:
        url_1 = url_paginator.page(url_paginator.num_pages)
    return render(request, 'scraper/history.html', {'urls' : url_1})

def detail(request):
    if request.method == 'POST':
        writer = request.POST.get("writer", None)
        title = request.POST.get("title", None)
        link = request.POST.get("link", None)
        date = request.POST.get("date", None)
        data = crawl_blog(link)
        text = article_text(link)
        obj = Blogs()
        print(data)
        print(text)
        obj.title = title
        obj.link = link
        obj.writer = writer
        obj.date = date
        obj.text = text
        obj.num_responses = data['num_responses']
        obj.num_claps = data['num_claps']
        obj.set_tags(data['related_tags'])
        obj.save()
        data['text'] = text
        data['link'] = link
        data['date_time'] = date
        data['writer'] = writer
        data['title'] = title
        print(data)
        if len(data) == 0:
            return render(request, "scraper/error.html", {'error' : 'Request Timeout'})
        return render(request, "scraper/detail.html", {'data' : data})
    else:
        return redirect(index)

def deletehistory(request):
    if request.method == "POST":
        id = request.POST['delete']
        try:
            check = Tags.objects.filter(id=id)
            check.delete()
            return redirect(history)
        except Tags.DoesNotExist:
            return redirect(history)
    else:
        return redirect('history')

def api(request):
    if not request.GET.get("tag"):
        return redirect(index)
    tag = str(request.GET.get("tag", None))
    tag = tag.replace(" ", "-")
    tag = tag.lower()
    tags = related_tags(tag)
    tag_db = Tags(tags=tag)
    tag_db.save()
    get_blog = []
    tags = related_tags(tag)
    i = 0
    while True:
        get_blog = get_blogs(tag)
        tags = related_tags(tag)
        if get_blog and tags:
            break
        if i == 7:
            break
        i = i + 1
    return JsonResponse({'data': get_blog, 'tags' : tags})