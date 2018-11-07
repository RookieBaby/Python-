from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
import time,os
from django.conf import settings
from fdfs_client.client import *
from django.utils.decorators import method_decorator
from .forms import PhotoForm
from .models import Photo,Types
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
# Create your views here.
import time,os,operator
import shutil
# def UploadMultis(request):
#     ChannelCode = Types.objects.all().order_by('ChannelCode')
#     return render(request,"UploadMulti/progress_bar_upload/indexs.html",{'ChannelCodes':ChannelCode})

def huoqu(request,tid):
    code_list = {'codes': tid}
    return render(request, "UploadMulti/progress_bar_upload/indexs.html", code_list)
class BasicUploadView(View):
    pass
class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        code_list = Types.objects.all().order_by('ChannelCode')
        a = []
        for code in code_list:
            ChannelCodes = code.ChannelCode
            if ChannelCodes.startswith('002') is True:
                a.append(ChannelCodes)
        dd = []
        cc = []
        for aa in a:
            if aa == '002':
                d = Types.objects.get(ChannelCode=aa)
                print(d)
                ChannelNames = d.ChannelName
                dd.append(ChannelNames)
            else:
                c = Types.objects.get(ChannelCode=aa)
                ChannelNames = c.ChannelName
                cc.append(ChannelNames)
        return render(self.request, 'UploadMulti/progress_bar_upload/index.html', {'photos': photos_list,'codes':cc,'dd':dd})
    def post(self, request):
        client = Fdfs_client('/etc/fdfs/client.conf')
        if request.method == 'POST':
            #获取上传图片视屏
            try:
                img_urls = request.FILES.getlist('file')
                #循环遍历写入项目静态文件media目录下
                for img_url in img_urls:
                    names = img_url.name
                    houzhui = names.split('.')
                    if houzhui[1] in '.vob,.ifo,.(DVD格式),.mpg,.mpeg,.dat,.mp4,.3gp,.mov,.rm,.ram,.rmvb,.wmv,.asf,.avi,.asx':
                        path1 = os.path.join(settings.MEDIA_ROOT, 'video', )
                        videos = os.listdir(path1)
                        names = img_url.name
                        if names not in videos:
                            path = os.path.join(settings.MEDIA_ROOT, 'video', img_url.name)
                            with open(path, 'wb') as pic:
                                for p in img_url.chunks():
                                    pic.write(p)
                        else:
                            print('已存在')
                    else:
                        path2 = os.path.join(settings.MEDIA_ROOT, 'photos', )
                        ptohos = os.listdir(path2)
                        names = img_url.name
                        if names not in ptohos:
                            path = os.path.join(settings.MEDIA_ROOT, 'photos', img_url.name)
                            with open(path, 'wb') as pic:
                                for p in img_url.chunks():
                                    pic.write(p)
                        else:
                            print('已存在')
                #获取静态目录地址
                path_2 = os.path.join(settings.MEDIA_ROOT, 'photos')
                path_1 = os.path.join(settings.MEDIA_ROOT, 'video')
                #获取静态目录下图片和视屏名称
                videos = os.listdir(path_1)
                photoss = os.listdir(path_2)
                #获取上传提交的类别名称
                codes = request.POST["types"]
                #根据名称获取类别对应code值
                lists = Types.objects.all().filter(ChannelName=codes)
                cd = []
                for cc in lists:
                    if '002' in cc.ChannelCode:
                        code = cc.ChannelCode
                        cd.append(code)
                codess = ''.join(cd)
                #以集合差集方式判断图片视屏是否对应
                pho = []
                vid = []
                for file2 in photoss:
                    pho1 = file2.split('.')[0]
                    pho.append(pho1)
                for file1 in videos:
                    vid2 = file1.split('.')[0]
                    vid.append(vid2)
                difference = list(set(pho)^set(vid))
                #不对应提示错误并且删除项目静态目录下文件

                if len(difference) > 0:
                    pvs = photoss + videos
                    PATH_NAME1 = os.path.join(settings.MEDIA_ROOT, 'photos', )
                    shutil.rmtree(PATH_NAME1)
                    os.makedirs(PATH_NAME1)
                    PATH_NAME2 = os.path.join(settings.MEDIA_ROOT, 'video', )
                    shutil.rmtree(PATH_NAME2)  # 创建一个文件夹
                    os.makedirs(PATH_NAME2)
                    ps = []
                    for pv in pvs:
                        for dif in difference:
                            if dif in pv:
                                ps.append(pv)
                    error_msg = '匹配失败,重新上传'
                    return render(request, 'UploadMulti/progress_bar_upload/index.html', {'info':ps,'error_msg': error_msg} )
                #匹配规则一致上传文件服务器fdfs和数据库
                else:
                    for file2 in photoss:
                        pho = file2.split('.')[0]
                        for file1 in videos:
                            vid = file1.split('.')[0]
                            if pho == vid:
                                filename1 = os.path.join(path_1, file1)
                                filename2 = os.path.join(path_2, file2)
                                ret1 = client.upload_by_filename(filename2)
                                ret2 = client.upload_by_filename(filename1)
                                photos_url = str(ret1['Remote file_id'], encoding="utf8")
                                videos_url = str(ret2['Remote file_id'], encoding="utf8")
                                os.remove(filename1)
                                os.remove(filename2)
                                Photo.objects.create(photos=photos_url, filename=vid, videos=videos_url, codes=codess, )
                return HttpResponseRedirect(reverse("UploadMulti:progress_bar_upload"))
            except:
                error_msg = '匹配失败,重新上传'
                return render(request, 'UploadMulti/progress_bar_upload/index.html',
                              {'error_msg': error_msg})
class DragAndDropUploadView(View):
    pass
    # codes.strip() == '':
    #     error_msg = '请输入类别code'
    #     return render(request, 'UploadMulti/progress_bar_upload/indexs.html', {'error_msg': error_msg})


def clear_database(request):
    PATH_NAME1 = os.path.join(settings.MEDIA_ROOT, 'photos', )
    shutil.rmtree(PATH_NAME1)
    os.makedirs(PATH_NAME1)
    PATH_NAME2 = os.path.join(settings.MEDIA_ROOT, 'video', )
    shutil.rmtree(PATH_NAME2)  # 创建一个文件夹
    os.makedirs(PATH_NAME2)
    return redirect(request.POST.get('next'))
def type_del(request,uid):
    client = Fdfs_client('/etc/fdfs/client.conf')
    ob = Photo.objects.get(id=uid)
    photo = ob.photos.name
    video = ob.videos.name
    vp = photo + ',' + video
    a = vp.split(',')
    for i in a:
        client.delete_file(i)
    ob.delete()
    return HttpResponseRedirect(reverse("UploadMulti:progress_bar_upload"))

# 后台首页
def index(request):
    return render(request,'UploadMulti/base.html')
def typeindex(request):
    # 执行数据查询，并放置到模板中
    list = Types.objects.extra(select={'t':'ChannelID+0'})
    list = list.extra(order_by=["t"])
    list = list.filter(ChannelCode__startswith="002")
    context = {"typeslist":list}
    return render(request,'UploadMulti/type/index.html',context)
# 类别信息添加表单
def typeadd(request):
    return render(request,'UploadMulti/type/add.html')
def typeinsert(request):
    ob = Types()
    b = []
    obs = Types.objects.values("ChannelID")

    for i in obs:
        a = int(i["ChannelID"])
        b.append(a)
    c = max(b)
    ob.ChannelID = str(c + 1)
    codes = Types.objects.values("ChannelCode")
    codes = codes.filter(ChannelCode__startswith="002")
    code_lists = []
    for code in codes:
        codess = code['ChannelCode']
        code_list = codess.split('.')
        if len(code_list) > 1:
            code_lists.append(int(code_list[1]))
    code_max = max(code_lists)
    ChannelCodes_max = (code_max + 1) / 1000 + 2
    ChannelCodes = '00' + str(ChannelCodes_max)
    ob.ChannelCode = ChannelCodes
    ChannelName = request.POST['ChannelName']
    ChannelNames = Types.objects.all().order_by('ChannelName')
    lists = []
    for c in ChannelNames:
        cc = c.ChannelName
        lists.append(cc)
    if ChannelName.strip() == '':
        error_msg = '类别名称不能为空'
        return render(request, 'UploadMulti/type/add.html', {'error_msg': error_msg})
    else:
        if ChannelName not in lists:
            ob.ChannelName = ChannelName
        else:
            error_msg = '类别名称已存在'
            return render(request, 'UploadMulti/type/add.html', {'error_msg': error_msg})

    #
    # ob.ChannelCode = request.POST['ChannelCode']
    ob.save()
    return HttpResponseRedirect(reverse("UploadMulti:UploadMulti_typeindex"))
def typedel(request,ChannelID):
    try:
        ob = Types.objects.get(ChannelID=ChannelID)
        ob.delete()
        return HttpResponseRedirect(reverse("UploadMulti:UploadMulti_typeindex"))
        # context = {'info': '删除成功！'}
    except:
        context = {'info': '删除失败！'}
    return render(request, "UploadMulti/info.html", context)
    # return HttpResponseRedirect(reverse("UploadMulti:UploadMulti_typeindex"))
def typeedit(request,ChannelID):
    try:
        ob = Types.objects.get(ChannelID=ChannelID)
        context = {'user': ob}
        return render(request, "UploadMulti/type/edit.html", context)
    except:
        context = {'info': '没有找到要修改的信息！'}
    return render(request, "UploadMulti/info.html", context)
def typeupdate(request,ChannelID):
    if request.method == 'POST':
        name = request.POST.get('ChannelNames')
        lists = Types.objects.filter(ChannelName=name)

        if lists:
            data = {'code': 1, 'msg': '类别名已存在'}
            return JsonResponse(data)
        ob = Types.objects.get(ChannelID=ChannelID)
        ChannelName = request.POST['ChannelName']
        ChannelNames = Types.objects.all().order_by('ChannelName')
        lists = []
        for c in ChannelNames:
            cc = c.ChannelName
            lists.append(cc)
        else:
            if ChannelName not in lists:
                ob.ChannelName = ChannelName
                ob.save()
            else:
                ob = Types.objects.get(ChannelID=ChannelID)
                error_msg = '类别名称已存在'
                context = {'user': ob, 'error_msg': error_msg}
                return render(request, "UploadMulti/type/edit.html", context,)
    return HttpResponseRedirect(reverse("UploadMulti:UploadMulti_typeindex"))

