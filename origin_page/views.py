from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils.timezone import now
from django.conf import settings
from django.http import JsonResponse
from .models import ImageFile 
import queue
import os


# 人机验证页面
def human_verification(request):
    """显示人机验证页面"""
    return render(request, 'human_verification.html')

# 验证成功后跳转到主界面
def verify_human(request):
    """处理验证并跳转到主界面"""
    # 这里可以添加更复杂的验证逻辑（如验证码）
    return redirect('main_page')

# 主界面
def main_page(request):
    """主界面"""
    return render(request, 'main_page.html')

# 上传图片
@csrf_exempt
def upload_image(request):

    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({"status": "error", "message": "No file uploaded"}, status=400)

        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        timestamp = now().strftime("%Y%m%d%H%M%S")
        unique_file_name = f"{timestamp}_{file_name}"

        file_path = default_storage.save(f"uploads/{unique_file_name}", ContentFile(uploaded_file.read()))
        
        # 记录到数据库
        image = ImageFile.objects.create(file_name=unique_file_name, file_path=file_path, status='pending')
        
        return JsonResponse({"status": "success", "file_path": file_path, "id": image.id, "file_name": unique_file_name})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

# 获取未处理的图片列表
@csrf_exempt
def get_unprocessed_images(request):
    if request.method == 'GET':
        images = ImageFile.objects.filter(status='pending')

        image_list = []
        for img in images:
            file_url = request.build_absolute_uri(f"{settings.MEDIA_URL}{img.file_path}")
            image_list.append({
                "id": img.id,
                "file_name": img.file_name,
                "file_url": file_url,
            })

        return JsonResponse({"status": "success", "images": image_list})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

# 确认图片已接收
@csrf_exempt
def mark_image_received(request):
    if request.method == 'POST':
        try:
            # 获取 image_id 列表
            image_ids = request.POST.getlist('image_id')
            success_count = 0
            for image_id in image_ids:
                try:
                    # 查找状态为 'pending' 的图片
                    image = ImageFile.objects.get(id=image_id, status='pending')
                    # 将图片状态标记为 'received'
                    image.status = 'received'
                    image.save()
                    success_count += 1
                except ImageFile.DoesNotExist:
                    continue
            if success_count > 0:
                return JsonResponse({"status": "success", "message": f"{success_count} images marked as received"})
            else:
                return JsonResponse({"status": "error", "message": "Image not found or already processed"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error processing request: {str(e)}"}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)



@csrf_exempt
def upload_processed_image(request):
    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        processed_file = request.FILES.get('file')

        if not image_id or not processed_file:
            return JsonResponse({"status": "error", "message": "Missing image_id or file"}, status=400)

        try:
            # 查找状态为 'received' 的图片
            image = ImageFile.objects.get(id=image_id, status='received')

            # 检查文件格式
            if not processed_file.name.endswith(('.jpg', '.jpeg', '.png')):
                return JsonResponse({"status": "error", "message": "Unsupported file type"}, status=400)

            # 创建处理后的文件保存路径
            processed_file_name = f"processed_{image.file_name}"
            processed_file_path = default_storage.save(f"processed/{processed_file_name}", ContentFile(processed_file.read()))

            # 更新图片状态为 'processed' 并保存处理文件路径
            image.status = 'processed'
            image.processed_file_path = processed_file_path  # 假设有字段保存处理后文件路径
            image.save()

            return JsonResponse({"status": "success", "file_path": processed_file_path})

        except ImageFile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Image not found or not in received state"}, status=404)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


def check_processed_image(request):
    file_name = request.GET.get('file_name')
    if not file_name:
        return JsonResponse({
            'status': 'error',
            'message': '缺少 file_name 参数',
        }, status=400)

    # 检查处理后的图像是否存在
    processed_file_name = f'processed_{file_name}'
    processed_file_path = os.path.join(settings.MEDIA_ROOT, 'processed', processed_file_name)

    if os.path.exists(processed_file_path):
        # 返回处理后的图像 URL
        return JsonResponse({
            "status": "ready",
            "file_url": f"{settings.MEDIA_URL}processed/{processed_file_name}",
        })
    else:
        # 图像仍在处理中
        return JsonResponse({
            "status": "processing",
            "message": "图像仍在处理中",
        })
