from django.urls import path
from . import views
app_name = 'AdminApp'
urlpatterns = [
    path('dashboard/',views.dashboard ,name='dashboard'),
    path('books/',views.books ,name='books'),
    path('analytics/',views.analytics ,name='analytics'),
    path('members/',views.members ,name='members'),
    path('requests/',views.requests ,name='requests'),
    path('ledger/',views.ledger ,name='ledger'),
    path('history/',views.history ,name='history'),
    path('Add/',views.Add ,name='Add'),
    path('update/<int:id>',views.update ,name='update'),
    path('logout/', views.logout, name='logout'),
    path('change_password',views.change_password,name='change_password'),
    path('edit/',views.edit ,name='edit'),
    path('delete_book/<int:id>',views.delete_book ,name='delete_book'),
    path('delete_member/<int:id>',views.delete_member ,name='delete_member'),
    path('approve_request/<int:id>',views.approve_request ,name='approve_request'),
    path('reject_request/<int:id>',views.reject_request ,name='reject_request'),
]