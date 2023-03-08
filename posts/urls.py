from django.urls import path
from posts import views


urlpatterns = [
    # must use .as_view because it is a class-based view
    path('posts/', views.PostList.as_view()),
]


# must add urlpatterns to main urls.py