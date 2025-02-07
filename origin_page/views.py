from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class LatestImageAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取 'uploads' 目录下最新上传的文件
        uploads_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(uploads_dir):
            return Response({"error": "上传目录不存在"}, status=404)

        files = os.listdir(uploads_dir)
        if not files:
            return Response({"error": "没有找到上传的文件"}, status=404)

        # 找到最新文件
        latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(uploads_dir, x)))
        file_url = os.path.join(settings.MEDIA_URL, 'uploads', latest_file)

        return Response({"latest_file_url": request.build_absolute_uri(file_url)})
    
def human_verification(request):
    """显示人机验证页面"""
    return render(request, 'human_verification.html')

def verify_human(request):
    """处理验证并跳转到主界面"""
    # 这里可以添加更复杂的验证逻辑（如验证码）
    return redirect('main_page')  # 跳转到主界面

def main_page(request):
    """主界面"""
    return render(request, 'main_page.html')

@csrf_exempt  # 确保跨站请求可以访问
def upload_image(request):
    print("收到上传请求")  # Debug: 确保 Django 视图被触发

    if request.method == 'POST':
        if 'file' not in request.FILES:
            print("错误：没有文件上传")  # Debug: 确保前端确实传了文件
            return JsonResponse({"status": "error", "message": "No file uploaded"}, status=400)

        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_file_name = f"{timestamp}_{file_name}"

        file_path = default_storage.save(f"uploads/{unique_file_name}", ContentFile(uploaded_file.read()))
        print(f"文件已保存: {file_path}")  # Debug: 确保文件成功存储

        return JsonResponse({"status": "success", "file_path": file_path})
    else:
        print("错误：请求方法错误")  # Debug: 确保请求是 POST
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)