from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
     path('',views.home ,name='home'),
     path('login/',views.login,name='login'),
     path('forgot/',views.forgot,name='forgot'),
     path('create/',views.create,name='create'),
     path('adminpanel/',include('AdminApp.urls',namespace='AdminApp')),
     path('user/', include(('UserApp.urls', 'UserApp'), namespace='UserApp')),
     path('admin/', admin.site.urls),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
