from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User
from scraper.models import Produto


class CustomAdminSite(admin.AdminSite):
    site_header = "MONITORAMENTO DE PREÇO DE PRODUTO"


admin_site = CustomAdminSite()
admin_site.register(Produto)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
