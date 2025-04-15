from django.contrib import admin
from scraper.models import Produto


class CustomAdminSite(admin.AdminSite):
    site_header = "MONITORAMENTO DE PREÇO DE PRODUTO"


admin_site = CustomAdminSite()
admin_site.register(Produto)
