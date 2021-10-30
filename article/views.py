from django.shortcuts import render, HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
# Create your views here.
from django.contrib import messages
from .models import Article,Comment
from django.contrib.auth.decorators import login_required


def articles(request):

    keyword = request.GET.get('keyword')
    
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request,"articles.html",{"articles":articles})


    articles = Article.objects.all()

    return render(request,"articles.html",{"articles":articles})

def index(request):

    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles":articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request, "Məqalə uğurla əlavə edildi.")
        return redirect("index")
    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article,id=id)

    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})
@login_required(login_url="user:login")
def updateArticle(request,id):

    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance=article)
    if article.author.id == request.user.id:
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            messages.success(request, "Məqalə uğurla güncəlləndi edildi.")
            return redirect("index")
    else:
        messages.warning(request,"Bu məqalə sizə aid deyil güncəlləyə bilməzsiniz!")
        return redirect("article:dashboard")


    return render(request,"update.html",{"form":form})
@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article, id = id)
    if article.author.id == request.user.id:
        article.delete()
        messages.success(request,message="Məqalə uğurla silindi.")
        return redirect("article:dashboard")
    else:
        messages.warning(request,"Bu məqalə sizə aid deyil silə bilməzsiniz!.")
        return redirect("article:dashboard")
    

def addComment(request,id):
    article = get_object_or_404(Article,id = id)

    if request.method == 'POST':
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        
        new_comment = Comment(comment_author = comment_author,comment_content=comment_content)

        new_comment.article = article
        messages.success(request,message="Şərh uğurla yazıldı.")
        new_comment.save()
    return redirect(reverse("article:detail",kwargs={"id":id}))