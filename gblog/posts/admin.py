from django.contrib import admin
from .models import Post, Image, Video, Tag

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "published"]
	list_display_links = ["updated"]
	list_filter = ["published"]
	list_editable = ["title"]
	search_fields = ["title", "content"]
	
	class Meta:
		model = Post

class ImageModelAdmin(admin.ModelAdmin):
	list_display = ["image_id", "slug", "image_alt"]
	list_display_links = ["image_id"]
	list_editable = ["slug", "image_alt"]

	class Meta:
		model = Image



admin.site.register(Post, PostModelAdmin)
admin.site.register(Image, ImageModelAdmin)
admin.site.register(Video)
admin.site.register(Tag)