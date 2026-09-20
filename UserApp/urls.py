from django.urls import path
from . import views
app_name='UserApp'

urlpatterns = [
    path('dashboard/',views.dashboard ,name='dashboard'),
    path('profile/',views.profile ,name='profile'),
    path('logout/', views.logout, name='logout'),
    path('change_password',views.change_password,name='change_password'),
    path('books_user/',views.books_user,name='books_user'),
    path('history_user/',views.history_user,name='history_user'),
    path('guide/',views.guide,name='guide'),
    path('terms/',views.terms,name='terms'),
    path('smart/',views.smart ,name='smart'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('request_book/<int:book_id>/',views.request_book,name='request_book'),
]
