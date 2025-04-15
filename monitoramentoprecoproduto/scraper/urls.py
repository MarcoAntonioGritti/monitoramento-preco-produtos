from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("scrape/", views.scrape_view, name="scrape"),
    path("", views.home_page_view, name="home"),
]
