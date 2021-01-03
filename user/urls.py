

from django.urls import path,include

from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('index', views.index,name="index"),
    path('register', views.register,name="register"),
    path('clienthome', views.clienthome,name="clienthome"),
    path('logout',views.logout,name="logout"),
    path('register_fir',views.register_fir,name="register_fir"),
    path('signature',views.signature,name="signature"),
    path('test',views.test,name="test"),
    path('clientcaserequest',views.clientcaserequest,name="clientcaserequest"),
    path('clientcasedetails',views.clientcasedetails,name="clientcasedetails"),
    path('clientcasehistory',views.clientcasehistory,name="clientcasehistory"),
    path('userprofile',views.userprofile,name="userprofile"),
    path('forgotpwd',views.forgotpwd,name="forgotpwd"),
    path('resetpwd',views.resetpwd,name="resetpwd"),
    path('validate_otp',views.validate_otp,name="validate_otp"),
    path('video_feed', views.video_feed, name='video_feed'),
    path('clientfirdownload', views.clientfirdownload, name='clientfirdownload'),
    path('getvolunteer', views.getvolunteer, name='getvolunteer'),
    path('useruploadaffidavit', views.useruploadaffidavit, name='useruploadaffidavit'),
    path('tryagain', views.tryagain, name='tryagain'),
    path('forgot_password',views.forgot_password,name="forgot_password"),
    path('email_sent',views.email_sent, name="email_sent"),
    path('reset_password',views.reset_password, name="reset_password"),
    path("userseleectmag", views.userseleectmag, name="userseleectmag"),

]
