from __future__ import unicode_literals
from django.conf import settings 
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone 
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.db.models import CASCADE

from markdown_deux import markdown

from .utils import get_read_time

STATUS_CHOICES = [
	('draft', 'Draft'),
	('published', 'Published'),
]


# Create your models here.

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager, self).filter(status='published')

def upload_location(instance, filename):
	return "%s/%s" %(instance.post_id, filename)

class Image(models.Model):
	image_id = models.AutoField(primary_key=True)
	blog = models.BooleanField(blank=True)
	image = models.ImageField(upload_to='images', null=True, blank=True)
	slug = models.SlugField(max_length=30, blank=False)
	image_alt = models.CharField(max_length=30, blank=True)
	image_credit = models.CharField(max_length=30, blank=True)

	def __str__(self):		
		return self.slug

class Post(models.Model):
	post_id = models.AutoField(primary_key=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=CASCADE)
	title = models.CharField(max_length=150)
	slug = models.SlugField(unique=True)
	description = models.CharField(max_length=200,null=True, blank=True)
	content = models.TextField()
	image = models.ForeignKey(Image, blank=True, null=True, on_delete=models.CASCADE)
	status = models.CharField(max_length=15, default='published', choices=STATUS_CHOICES)
	read_time = models.IntegerField(default=0)
	published = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	objects = PostManager()

	def __str__(self):		
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})

	class Meta:
		ordering = ["-published", "-updated"] 

	def get_markdown(self):
		content = self.content
		markdown_text = markdown(content)
		return mark_safe(markdown_text)


# def create_slug(instance, new_slug=None):
# 	slug = slugify(instance.title)
# 	if new_slug is not None:
# 		slug = new_slug
# 	qs = Post.objects.filter(slug=slug).order_by("-id")
# 	exists = qs.exists()
# 	if exists:
# 		new_slug = "%s-%s" %(slug, qs.first().id)
# 		return create_slug(instance, new_slug=new_slug)
# 	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs): 
	# if not instance.slug:
	# 	instance.slug = create_slug(instance)

	if instance.content:
		html_string = instance.get_markdown()
		read_time_var = get_read_time(html_string)
		instance.read_time = read_time_var

pre_save.connect(pre_save_post_receiver, sender=Post)