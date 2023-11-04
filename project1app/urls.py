from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.index,name='index'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('login',views.login,name='login'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('welcome',views.welcome,name='welcome'),
    path('adminlogin',views.adminlogin,name='adminlogin'),
    path('admindashboard',views.admindashboard,name='admindashboard'),
    path('index',views.index,name='index'),
    path('management',views.management,name='management'),
    path('addnotice',views.addnotice,name='addnotice'),
    path('viewcomplaints',views.viewcomplaints,name='viewcomplaints'),
    path('viewpayment',views.viewpayment,name='viewpayment'),
    path('photo',views.photo,name='photo'),
    path('userphoto',views.userphoto,name='userphoto'),
    path('Addmember',views.Addmember,name='Addmember'),
    path('noticeboard',views.noticeboard,name='noticeboard'),
    path('complaint',views.complaint,name='complaint'),
    path('payment',views.payment,name='payment'),
    path('loadimages',views.loadimages,name='loadimages'),
    path('Updatemember/<str:id>/',views.Updatemember,name='Updatemember'),
    path('Deletemember/<str:id>/',views.Deletemember,name='Deletemember'),
    path('photogallery',views.photogallery,name='photogallery'),
    path('userphotogallery',views.userphotogallery,name='userphotogallery'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('logout',views.logout,name='logout')



    



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)