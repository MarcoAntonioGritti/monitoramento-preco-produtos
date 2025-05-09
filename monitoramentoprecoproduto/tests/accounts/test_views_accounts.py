from http import HTTPStatus

import pytest
from accounts.view import login_view
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_view_pagina_login(client):

    url = reverse("accounts:login")
    response = client.get(url)

    template_usado = [t.name for t in response.templates]

    # Verifica se o template correto está sendo usado
    assert "accounts/login.html" in template_usado

    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == HTTPStatus.OK

    # Verifica se o nome da url corresponde ao nome esperado
    assert response.resolver_match.view_name == "accounts:login"

    # Verifica se a view correspondente é a esperada
    assert response.resolver_match.func == login_view.authenticate_user


@pytest.mark.django_db
def test_view_pagina_login_post(client):
    # Cria um usuário para o teste
    User.objects.create_user(username="testuser", password="testpassword")

    url = reverse("accounts:login")
    response = client.post(url, {"username": "testuser", "password": "testpassword"})

    # Verifica se o redirecionamento ocorreu corretamente
    assert response.status_code == HTTPStatus.FOUND  # 302
    assert response.url == reverse(
        "scraper:inicio"
    )  # Redireciona para a página inicial após login bem-sucedido

    # Verifica se o usuário está autenticado
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_view_pagina_login_post_invalid(client):
    # Cria um usuário para o teste
    User.objects.create_user(username="testuser", password="testpassword")

    url = reverse("accounts:login")
    response = client.post(url, {"username": "testuser", "password": "wrongpassword"})

    # Verifica se o status da resposta é 200 (OK) e se a mensagem de erro está presente
    assert response.status_code == HTTPStatus.OK
    assert "Usuário ou senha inválidos!." in response.content.decode()

    # Verifica se o usuário não está autenticado
    assert not response.wsgi_request.user.is_authenticated
