from django.shortcuts import render,get_object_or_404,redirect
from .models import Blog,Comment,Like
from django.utils import timezone
# Create your views here.
def blog(request):
    blogs = Blog.objects.all()
    return render(request,'blog.html', { 'blogs' : blogs })

# R
def detail(request, blog_id):
    detail = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.all().filter(post = detail)

    #좋아요 기능
    user=request.user #현재 유저

    if detail.likes.filter(id=user.id): #현재 유저가 likes에 존재하는 순서쌍들 중에 있다면 ->좋아요를 눌렀다는 뜻.
        message="좋아요 취소"
    else:
        message="좋아요"
    return render(request ,'detail.html', { 'detail' : detail, 'comments': comments , 'message' : message } )


def new(request):
    return render(request, 'new.html')

def create(request):
    blog = Blog() # 객체 틀 하나 가져오기
    blog.title = request.GET['title']  # 내용 채우기
    blog.body = request.GET['body'] # 내용 채우기
    blog.pub_date = timezone.datetime.now() # 내용 채우기
    blog.writer = request.user
    blog.save() # 객체 저장하기

    # 새로운 글 url 주소로 이동
    return redirect('/blog/' + str(blog.id))

#삭제
def delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('/blog/')
#update

def update(request, blog_id):
    blog = get_object_or_404(Blog, pk =blog_id)

    if request.method == "POST":
        blog.title = request.POST['title']
        blog.body = request.POST['body']
        blog.pub_date = timezone.datetime.now()
        blog.save()
        return redirect('/blog/' +str(blog.id))
    else:
        return render(request,'update.html')

def comment(request, blog_id):
    if request.method == "POST":
        comment = Comment()
        comment.body = request.POST['body']
        comment.c_writer = request.user
        comment.pub_date = timezone.datetime.now()
        comment.post = get_object_or_404(Blog, pk=blog_id)
        comment.save()
        
        return redirect('/blog/'+str(blog_id))
    else:
        return redirect('/blog/'+str(blog_id))


def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    blog_id = comment.post.id

    comment.delete()

    return redirect('/blog/'+str(blog_id))

def post_like(request, blog_id):
    user=request.user

    blog=get_object_or_404(Blog, pk=blog_id)

    if blog.likes.filter(id = user.id):
        blog.likes.remove(user)
    else:
        blog.likes.add(user)

    return redirect('/blog/'+str(blog_id))