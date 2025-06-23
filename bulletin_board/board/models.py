from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from datetime import timedelta
import random


# Категории объявлений
CATEGORIES = [
    ('tank', 'Танки'),
    ('healer', 'Хилы'),
    ('dd', 'ДД'),
    ('trader', 'Торговцы'),
    ('gm', 'Гилдмастеры'),
    ('quest', 'Квестгиверы'),
    ('smith', 'Кузнецы'),
    ('leather', 'Кожевники'),
    ('potion', 'Зельевары'),
    ('spell', 'Мастера заклинаний'),
]

# Объявление
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=128)
    content = RichTextUploadingField()  # WYSIWYG
    category = models.CharField(max_length=20, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.author.username})'


# Отклик на объявление
class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='responses')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)


    def __str__(self):
        return f'Отклик от {self.author.username} на "{self.post.title}"'


# Одноразовый код подтверждения e-mail
class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Код для {self.user.email}: {self.code}'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(random.randint(10000, 99999))
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=10)
class Ad(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title