from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path('group/<slug>', views.group_post),
    path('new/', views.new_post, name='new_post'),
    path("<username>/<int:post_id>/", views.post_view, name="post"),
    path("<username>/<int:post_id>/edit", views.post_edit, name="post_edit"),
    path("<username>/", views.profile, name="profile"),
]
