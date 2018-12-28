from django.db import models
import markdown
from django.utils.html import strip_tags
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

from  django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

@python_2_unicode_compatible
class Post2(models.Model):
    body = RichTextUploadingField(verbose_name='正文')


@python_2_unicode_compatible
class Category(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    flag_name= ((1,'显示'),
               (2,'隐藏'),)
    title = models.CharField(u'标题',max_length=70)
    body = RichTextUploadingField(u'内容')
    created_time = models.DateTimeField(u'发表时间', editable = True)
    modified_time = models.DateTimeField(u'更新时间', null=True,auto_now=True)
    # 文章摘要
    excerpt = models.CharField(u'摘要',max_length=200, blank=True)
    # 文章分类标签
    category = models.ForeignKey('Category')
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者，这里从User 是从Django.contrib.auth.models 导入

    author = models.ForeignKey(User)
    views = models.PositiveIntegerField(default=0)
    flag = models.IntegerField('标记',choices=flag_name)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(
                extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                ]
            )
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        super(Post, self).save(*args, **kwargs)


