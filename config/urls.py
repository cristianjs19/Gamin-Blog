from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

# from posts import views
from accounts.views import AccountCreateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/', AccountCreateView.as_view(), name='register'),
    url(r'^login/', LoginView.as_view(template_name='form.html', extra_context={'title':'Login'}), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^', include(("posts.urls", "posts"), namespace='posts')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]