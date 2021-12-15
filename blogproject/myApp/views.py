from django.shortcuts import render,get_object_or_404
from myApp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from myApp.forms import EmailSendForm,CommentForm
from myApp.models import Comment
from django.core.mail import send_mail
from myApp.models import Post
from taggit.models import Tag
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)#provided slug
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,2) #step1
    page_number=request.GET.get('page') #step2
    try:
        post_list=paginator.page(page_number) #step2
    except PageNotAnInteger:
        post_list=paginator.page(1) #step3
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages) #step4
    d={'post_list':post_list}
    return render(request,'myApp/post_list.html',d)
def post_details_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    form=CommentForm()
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            newcomment=form.save(commit=False)
            newcomment.post=post
            newcomment.save()
            csubmit=True
    d={'post':post,'form':form,'csubmit':csubmit,'comments':comments}
    return render(request,'myApp/post_details.html',d)
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    form=EmailSendForm()
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            #read the data send mail
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{0}[{1}]recommends you to read {2}'.format(cd['name'],cd['email'],post.title)
            message="Read Post At \n {0}\n\n{1} comments \n{2}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'varunabvs79@gmail.com',[cd['to']])
    d={'post':post,'form':form}
    return render(request,'myApp/sharebymail.html',d)
# Create your views here.
