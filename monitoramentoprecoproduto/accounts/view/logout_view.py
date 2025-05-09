from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse("accounts:login"))
