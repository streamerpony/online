"""online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path
from . import views
from .views import LatestImageAPIView


urlpatterns = [
    path('', views.human_verification, name='human_verification'),  # 人机验证页面
    path('verify-human/', views.verify_human, name='verify_human'),  # 处理验证
    path('main/', views.main_page, name='main_page'),  # 主界面
    path('upload-image/', views.upload_image, name='upload_image'),
    path('api/latest-image/', LatestImageAPIView.as_view(), name='latest-image')
]