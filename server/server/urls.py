from django.contrib import admin
from django.urls import path, include, re_path
from frontend.views import serve_react
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path( r"^api/static/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    path('api/', include('api.urls')),
    re_path(r"^(?P<path>.*)$", serve_react, {"document_root": settings.REACT_APP_BUILD_PATH}),
] + static(settings.REACT_STATIC_BASEURL, document_root=settings.REACT_STATICFILES_DIR)

