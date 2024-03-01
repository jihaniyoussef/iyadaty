from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', include('first_app.urls')),
    path('', include('consultation.urls')),
    path('', include('statchart.urls')),
    path('consultation/', include('appcon.urls')),
]

# Configure Admin Titles
admin.site.site_header = "3iyadati administration"
admin.site.site_title = "3iyadati"
admin.site.index_title = "Welcome to the administration page"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
