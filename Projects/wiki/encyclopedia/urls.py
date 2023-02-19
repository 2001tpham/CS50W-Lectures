from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.page_render, name='entry_page'),
    path('search/', views.search, name='search'),
    path('create-page/', views.render_create_page, name='create'),
    path('edit/', views.edit_page, name='edit'),
    path('edit-submit', views.edit_submit, name='edit_submit'),
    path('random/', views.random, name='random')
]
