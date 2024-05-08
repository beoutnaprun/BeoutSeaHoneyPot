"""
URL configuration for djangoHonWeb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from Index import views
from api import views as apiviews
from webAdmin import views as adminViews

urlpatterns = [
    # 蜜罐理由
    path('', views.index_view),
    path('index', views.index_view,name='index'),
    path('Register', views.register_view),
    path('index/captcha', views.index_captcha),
    path('api/phoneSMS', apiviews.phoneSMS),
    path('api/phoneSMSReg', apiviews.phoneSMSReg),
    path('api/login', apiviews.Login),
    # 管理员接口
    path('webAdmin', adminViews.login),
    path('webAdmin/Index', adminViews.index),
    path('webAdmin/LoginOut', adminViews.LoginOut),
    path('api/delete/attack', adminViews.Delete_Attack),
    path('api/delete/user', adminViews.Delete_User),
    path('api/webSetting/save', adminViews.WebConfig),
    path('api/edit/passwd', adminViews.Edit_Passwd),
    # 通用路由
    path('api/view', adminViews.view),
]

handler404 = 'Index.views.page_not_found'  # 指定自定义的 404 错误处理视图
