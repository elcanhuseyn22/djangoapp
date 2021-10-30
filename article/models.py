from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete=models.CASCADE)
    title = models.CharField(verbose_name="Başlıq",max_length=50)
    content = RichTextField(verbose_name="Məzmun")
    created_at = models.DateTimeField(auto_now_add=True)
    article_image = models.FileField(blank=True,null=True,verbose_name = "Şəkil əlavə et")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name = "Məqalə",related_name="comments")
    comment_author = models.CharField(max_length=50,verbose_name="Ad")
    comment_content = models.CharField(verbose_name="Şərh",max_length=200)
    comment_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_at']
