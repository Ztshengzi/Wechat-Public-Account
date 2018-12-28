from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from django.http import HttpResponse
from .models import Post, Category, Tag
from .pagination import pagination
from django.db.models import Q
from django.views.decorators.cache import cache_page
import json
import time as time1
from weixin.get12306.get12306 import get_query_url, GetInfoTrain
from weixin.models import ParseStation,UserInfo,UserLocation
from django.contrib.auth.decorators import login_required



def test(request):
    return render(request, 'weixin/test.html', )

@login_required()
def getruning(request):
    """
    :param request:
    :return: 获取位置信息并返回
    """
    if request.method== "GET":
        userinfos = UserInfo.objects.filter().all()
        return render(request,"weixin/get_runing.html",{'userinfos':userinfos,})
    if request.method =="POST":
        userid = request.POST.get('id')
        localtion_list=[]
        user_localtions = UserLocation.objects.filter(user_id=userid).order_by('-createTime')[0:1000]
        for localtion in user_localtions:
            localtion_list.insert(0,[float(localtion.Longitude),float(localtion.Latitude)])
        localtion_list_dic = json.dumps({'localtion_data':localtion_list,})
        return HttpResponse(localtion_list_dic)



def ajax_info(request):
    if request.method == "POST":
        username = request.POST.get('username', '芜湖')
        print(username)
        return HttpResponse


train_station = ParseStation.objects.all()


def train(request):
    if request.method == 'GET':
        time = request.GET.get('time', time1.strftime('%Y-%m-%d', time1.localtime(time1.time())))
        place = request.GET.get('place', '上海')
        destination = request.GET.get('destination', '北京')
        dic = {'time': time, 'place': place, 'destination': destination}
        str = time + ' ' + place + ' ' + destination
        url = get_query_url(str)
        content = GetInfoTrain(url, True)
        return render(request, 'weixin/train.html',
                      {'train_station': train_station, 'content': content, "dic": json.dumps(dic)})
    if request.method == 'POST':
        time = request.POST.get('time')
        place = request.POST.get('place')
        destination = request.POST.get('destination')
        # print('时间:'+time)
        # print('出发地:'+place)
        # print('目的地:'+destination)
        str = time + ' ' + place + ' ' + destination
        url = get_query_url(str)
        content = GetInfoTrain(url, True)
        # dic = {'time': time, 'place': place, 'destination': destination}
        return HttpResponse(json.dumps(content))


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q),flag=1)
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    URL = request.get_host() + request.path
    print(URL)
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list,
               'URL': URL
               }
    return render(request, 'blog/detail.html', context=context)


@cache_page(60 * 15)
def archives(request, year, month):
    # print(year,month)
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    flag=1).order_by('-created_time')
    # for post in post_list:
    #     print(post.title)

    return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(pagination):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    def get_queryset(self):
        return super(IndexView,self).get_queryset().filter(flag=1)

class ArchiivesView(pagination):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return super(ArchiivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                                created_time__month=self.kwargs.get('month'),
                                                                flag=1)


class CategoryView(pagination):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(pagination):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def genrate_qrcode(request, data):
    import qrcode
    img = qrcode.make(data)
    from django.utils.six import BytesIO
    buf = BytesIO()
    img.save(buf)
    imge_stream = buf.getvalue()

    response = HttpResponse(imge_stream, content_type='image/png')
    return response
