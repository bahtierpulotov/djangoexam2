from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    
    path('list_category/', list_category, name='list_category'),
    path('add_category/', create_category, name='add_category'),
    path('update_category/<int:id>/', update_category, name='update_category'),
    path('delete_category/<int:id>/', delete_category, name='delete_category'),
    path('detail_category/<int:id>/', detail_category, name='detail_category'),


    path('list_author/', list_author, name='list_author'),
    path('add_author/', create_author, name='add_author'),
    path('update_author/<int:id>/', update_author, name='update_author'),
    path('delete_author/<int:id>/', delete_author, name='delete_author'),
    path('detail_author/<int:id>/', detail_author, name='detail_author'),

    
    path('list_book/', list_book, name='list_book'),
    path('add_book/', create_book, name='add_book'),
    path('update_book/<int:id>/', update_book, name='update_book'),
    path('delete_book/<int:id>/', delete_book, name='delete_book'),
    path('detail_book/<int:id>/', detail_book, name='detail_book'),


    path('list_review/<int:book_id>/', list_review, name='list_review'),
    path('add_review/<int:book_id>/', create_review, name='add_review'),
    path('update_review/<int:id>/', update_review, name='update_review'),
    path('delete_review/<int:id>/', delete_review, name='delete_review'),
    path('detail_review/<int:id>/', detail_review, name='detail_review'),

    path('statistics/', statistics, name='statistics'),

    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', log_out, name='logout'),
    path('change_password/', change_password, name='change_password'),
    path('reset/<uuid:token>/', reset_confirm, name='reset_password'),
    path('reset_request/', reset_request, name='reset_request'),
    path('verify/<uuid:token>/', verify_email, name='verify_email'),
]
