
from django.contrib import admin
from django.urls import path, include
# ! for images
from django.conf.urls.static import static
from django.conf import settings

# 👇 One-time superuser creation
from django.contrib.auth import get_user_model
from django.db.utils import OperationalError

try:
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "zahidulturja@gmail.com", "admin123!")
        print("✅ Superuser created.")
except OperationalError:
    # Happens before migrations, ignore silently
    pass

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("devedu.urls")),
    path("", include("django.contrib.auth.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
