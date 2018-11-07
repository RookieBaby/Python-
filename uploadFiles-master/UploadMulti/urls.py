from django.conf.urls import url
from . import views
app_name = 'UploadMulti'
#(?P<codes>\d+(\.\d+))
urlpatterns = [
    url(r'^clear/$', views.clear_database, name='clear_database'),
    url(r'^huoqu/(?P<tid>.*)/$', views.huoqu, name='huoqu'),
    url(r'^type_del/(?P<uid>[0-9]+)$', views.type_del, name="type_del"),
    url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
    url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
    url(r'^$', views.ProgressBarUploadView.as_view(), name="progress_bar_upload"),
    url(r'^type/$', views.typeindex, name="UploadMulti_typeindex"),
    url(r'^typeadd/$', views.typeadd, name="UploadMulti_typeadd"),
    url(r'^typeinsert$', views.typeinsert, name="UploadMulti_typeinsert"),
    url(r"^typedel/(?P<ChannelID>.*)$", views.typedel, name="UploadMulti_typedel"),
    url(r'^typeedit/(?P<ChannelID>.*)$', views.typeedit, name="UploadMulti_typeedit"),
    url(r'^typeupdate/(?P<ChannelID>.*)$', views.typeupdate, name="UploadMulti_typeupdate")

]