from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog
from django.utils import timezone
# Create your views here.
def home(request):
    blogs = Blog.objects.all()
    return render(request,'home.html', { 'blogs' : blogs })

# R
def detail(request, blog_id):
    detail = get_object_or_404(Blog, pk=blog_id)
    return render(request ,'detail.html', { 'detail' : detail } )


def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog() # 객체 틀 하나 가져오기
    blog.title = request.GET['title']  # 내용 채우기
    blog.body = request.GET['body'] # 내용 채우기
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.save() # 객체 저장하기

    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))
