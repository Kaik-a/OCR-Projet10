"""Views for accounts"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from search.navbar_decorator import navbar_search_decorator

from .forms import LoginForm, SubscribeForm


def login_user(request, form: LoginForm) -> HttpResponse:
    """
    Verify login.

    :param request: django request
    :param LoginForm form: form to retrieve login data
    :return: HttpResponse
    """
    # Get credentials
    username = form.data.get("login")
    password = form.data.get("password")

    if username and password:
        # Authenticate with given credentials
        user: User = authenticate(
            username=username,
            password=password,
        )
        # A user exists with given credentials
        if user:
            login(request, user)
            messages.add_message(
                request, 25, f"Bonjour {user.first_name}! Vous êtes maintenant connecté"
            )
            return redirect(reverse("accounts:user_account"))

        # No user found
        messages.add_message(
            request,
            40,
            "Aucun compte recensé avec cette combinaison. Votre email ou mot de "
            "passe sont peut être incorrects?",
        )
        return render(request, "login.html", {"form": form})

    return render(request, "login.html", {"form": form})


@navbar_search_decorator
def get_user_info(request) -> HttpResponse:
    """
    View to send login data.

    :param request: django request
    :return: HttpResponse
    """
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            return login_user(request, form)
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@navbar_search_decorator
def subscribe(request) -> HttpResponse:
    """
    View to subscribe for a new user.

    :param request: django request
    :return: HttpResponse
    """
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            try:
                User.objects.create_user(
                    username=form.data.get("login"),
                    password=form.data.get("password"),
                    first_name=form.data.get("first_name"),
                    last_name=form.data.get("last_name"),
                    email=form.data.get("email"),
                )
                messages.add_message(
                    request,
                    25,
                    f"L'utilisateur {form.data.get('login')} a bien été créé, "
                    f"vous pouvez dès à présent vous connecter",
                )
            except IntegrityError as error:
                messages.add_message(
                    request, 40, f"Echec lors de la création du compte: {error}"
                )
            form_connect = LoginForm()

            return redirect(reverse("accounts:login"), form=form_connect)
    else:
        form = SubscribeForm()

    return render(request, "subscribe.html", {"form": form})


@login_required
def sign_out(request) -> HttpResponse:
    """
    View to log out.

    :param request: django request
    :return: HttpResponse
    """
    logout(request)

    messages.add_message(request, 25, "Au revoir!")
    return redirect(reverse("home"))


@navbar_search_decorator
@login_required
def user_account(request) -> HttpResponse:
    """
    View to get user accounts.

    :param request: django request
    :return: HttpResponse
    """
    return render(request, "user_account.html")
