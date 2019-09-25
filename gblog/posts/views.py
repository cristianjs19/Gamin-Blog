try:
    from urllib.parse import quote_plus 
except: 
    pass

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


from .models import Post
from .forms import PostForm
from .utils import get_read_time

from .utils import get_read_time

# Create your views here.
def post_create(request):
	if not request.user.is_authenticated:
		response = HttpResponse("Must be logged to proceed.")
		response.status_code = 403
		return response
	if not request.user.is_staff:
		response = HttpResponse("Must be staff member to proceed.")
		response.status_code = 403
		return response
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid() and request.user.is_authenticated:
		instance = form.save(commit=False)
		instance.user = request.user 
		instance.save()
		messages.success(request, "Post created successfully!")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form": form
	}
	return render(request, "post_form.html", context)


def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.publish > timezone.now().date() or instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.titulo)
	print(get_read_time(instance.get_markdown()))
	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id,
	}
	
	context = {
		"titulo": instance.titulo,
		"instance": instance,
		"share_string": share_string,
		
	}
	return render(request, "post_detail.html", context)


def post_list(request):
	hoy = timezone.now().date()
	queryset_list = Post.objects.active() #filter(draft=False).filter(publish__lte=timezone.now()) #all() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
		
	paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
	page_request_var = "list"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
	"titulo": "Super Gaming Blog!",
	"object_list": queryset,
	"page_request_var": page_request_var,
	"hoy": hoy,
	}

	return render(request, "post_list.html", context)

def post_update(request, slug=None):
	if not request.user.is_authenticated:
		response = HttpResponse("Must be logged to proceed.")
		response.status_code = 403
		return response
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "<a href='#'>Post</a> Successfully edited.", extra_tags="html_safe")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"titulo": instance.titulo,
		"instance": instance,
		"form": form,
	}
	return render(request, "post_form.html", context)


def post_delete(request, slug=None):
	if not request.user.is_authenticated:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Post deleted.")
	return redirect("posts:list")