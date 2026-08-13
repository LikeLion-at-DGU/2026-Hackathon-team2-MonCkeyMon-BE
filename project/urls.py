from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/', include('experiences.urls')),
    path('api/', include('products.urls')),
    path('api/', include('delivery.urls')),
]

# 개발 환경에서 media 파일 접근 허용
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)