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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 前端界面路由
    path('', views.human_verification, name='human_verification'),  # 默认访问人机验证
    path('verify/', views.verify_human, name='verify_human'),  # 验证后跳转
    path('main/', views.main_page, name='main_page'),  # 进入主界面

    # API 路由
    path('api/upload/', views.upload_image, name='upload_image'),  # 上传原始图片
    path('api/unprocessed/', views.get_unprocessed_images, name='get_unprocessed_images'),  # 获取未处理图片列表
    path('api/mark_received/', views.mark_image_received, name='mark_image_received'),  # 确认图片已接收
    path('api/upload_processed/', views.upload_processed_image, name='upload_processed_image'),  # 上传已处理图片
    path('api/check_processed_image/', views.check_processed_image, name='check_processed_image'),#前端检测图片是否已处理
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)