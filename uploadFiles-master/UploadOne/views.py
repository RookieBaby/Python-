from django.shortcuts import render,redirect
from uploadFiles import settings
from django.core.files.storage import FileSystemStorage
import os
from .models import Document
from .forms import DocumentForm
# Create your views here.
from fdfs_client.client import *
def home(request):
    documents = Document.objects.all()
    return render(request, 'UploadOne/home.html', { 'documents': documents })

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('UploadOne:home')
    else:
        form = DocumentForm()
    return render(request, 'UploadOne/model_form_upload.html', {
        'form': form
    })


def simple_upload(request):
    client = Fdfs_client('/etc/fdfs/client.conf')
    if request.method == 'POST' and request.FILES['myfile']:
        img_url = request.FILES['myfile']
        fs = FileSystemStorage()
        # img_url = fs.save(myfile.name, myfile)
        baseDir = os.path.dirname(os.path.abspath(__name__))
        jpgdir = os.path.join(baseDir, 'media/photos')
        filename = os.path.join(jpgdir, img_url.name)
        ret = client.upload_by_filename(filename)
        new_url = str(ret['Remote file_id'], encoding="utf8")
        uploaded_file_url = fs.url(new_url)
        print(uploaded_file_url,10101010101)
        return render(request, 'UploadOne/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'UploadOne/simple_upload.html')
