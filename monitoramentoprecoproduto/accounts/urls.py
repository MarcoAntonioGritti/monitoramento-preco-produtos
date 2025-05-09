from django.urls import path

from .view import login_view, logout_view

app_name = "accounts"
urlpatterns = [
    path("login/", login_view.authenticate_user, name="login"),
    path("logout/", logout_view.logout_user, name="logout"),
]
