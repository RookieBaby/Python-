from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views import View
import time,os
from django.conf import settings
from fdfs_client.client import *
from django.utils.decorators import method_decorator
from .forms import PhotoForm
from .models import Photo,Types
from django.http import HttpResponse
# Create your views here.
import time,os
import shutil
import os

import shutil
def huoqu(request,tid):
    code_list = {'codes': tid}
    return render(request, "UploadMulti/progress_bar_upload/index.html", code_list)
class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'UploadMulti/basic_upload/index.html', {'photos': photos_list})

    def post(self, request):
        client = Fdfs_client('/etc/fdfs/client.conf')
        if request.method == 'POST':
            img_urls = request.FILES.getlist('file')
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
        path_2 = os.path.join(settings.MEDIA_ROOT, 'photos')
        path_1 = os.path.join(settings.MEDIA_ROOT, 'video')
        videos = os.listdir(path_1)
        photoss = os.listdir(path_2)
        codes = request.POST["types"]
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
                    Photo.objects.create(file=photos_url, videoname=vid, file2=videos_url,codes=codes,)
                    print('文件已上传')
        return render(self.request, 'UploadMulti/basic_upload/index.html',)
class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'UploadMulti/progress_bar_upload/index.html', {'photos': photos_list})
    def post(self, request):
        client = Fdfs_client('/etc/fdfs/client.conf')
        if request.method == 'POST':
            img_urls = request.FILES.getlist('file')
            for img_url in img_urls:
                try:
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
                    path_2 = os.path.join(settings.MEDIA_ROOT, 'photos')
                    path_1 = os.path.join(settings.MEDIA_ROOT, 'video')
                    videos = os.listdir(path_1)
                    photoss = os.listdir(path_2)
                    codes = request.POST["types"]
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
                                Photo.objects.create(file=photos_url, videoname=vid, file2=videos_url, codes=codes, )
                                os.remove(filename2)
                                os.remove(filename1)
                                context = {'info': '添加成功！'}
                        return render(self.request, 'UploadMulti/basic_upload/index.html',)

                except:
                    print(123)

class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'UploadMulti/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        client = Fdfs_client('/etc/fdfs/client.conf')
        if request.method == 'POST':
            img_urls = request.FILES.getlist('file')
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
            path_2 = os.path.join(settings.MEDIA_ROOT, 'photos')
            path_1 = os.path.join(settings.MEDIA_ROOT, 'video')
            videos = os.listdir(path_1)
            photoss = os.listdir(path_2)
            codes = request.POST["types"]
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
                        Photo.objects.create(file=photos_url, videoname=vid, file2=videos_url, codes=codes, )
            return render(self.request, 'UploadMulti/basic_upload/index.html', )
def clear_database(request):
    PATH_NAME1 = os.path.join(settings.MEDIA_ROOT, 'photos', )
    shutil.rmtree(PATH_NAME1)
    os.makedirs(PATH_NAME1)
    PATH_NAME2 = os.path.join(settings.MEDIA_ROOT, 'video', )
    shutil.rmtree(PATH_NAME2)  # 创建一个文件夹
    os.makedirs(PATH_NAME2)
    return redirect(request.POST.get('next'))

 # 将整个文件夹删除
 #
 #    os.makedirs(PATH_NAME)  # 重新创建文件夹

    # for photo in Photo.objects.all():
    #     photo.file.delete()
    #     photo.delete()
    # return redirect(request.POST.get('next'))
def type_del(request,uid):
    client = Fdfs_client('/etc/fdfs/client.conf')
    try:
        ob = Photo.objects.get(id=uid)
        photo = ob.file.name
        video = ob.file2.name
        vp = photo + ',' + video
        a = vp.split(',')
        for i in a:
            client.delete_file(i)
        ob.delete()
        context = {'info': '删除成功！'}
    except Exception as e:
        context = {'info': '删除失败！'}
    return render(request, "UploadMulti/info.html", context)
