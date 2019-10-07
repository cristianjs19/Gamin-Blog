from django.views.generic import ListView, DetailView

from .models import Post

class PostListView(ListView):
	paginate_by = 2
	template_name = "post_list.html"

	def get_context_data(self, *args, **kwargs):
		context = super(PostListView, self).get_context_data(*args, **kwargs)
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		if request.user.is_authenticated:
			return Post.objects.all()
		else:
			return Post.objects.active()

class PostDetailView(DetailView):
	queryset = Post.objects.all()
	template_name = 'post_detail.html'

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		return context

	def get_object(self, *args, **kwargs):
		request = self.request
		slug = self.kwargs.get('slug')
		obj = Post.objects.get(slug=slug)
		return obj



