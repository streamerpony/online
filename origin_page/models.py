from django.db import models

class ImageFile(models.Model):
    STATUS_CHOICES = [
        ('pending', '未处理'),
        ('received', '已接收'),
        ('processed', '已处理')
    ]

    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=512)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} ({self.get_status_display()})"
