from django.contrib.auth import (logout,
                                 login)
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from User.forms import authForm
from django.contrib import messages


@csrf_protect
def login_system(request):
    form = authForm()
    try:
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')

        if request.method == "POST":
            form = authForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request,
                                    username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('user:initial_page')
                else:
                    messages.warning(request, "Usuario ou Senha Errados.")
            else:
                messages.warning(request, "Credenciais inválidas.")
    except Exception as e:
        print(f"Exceção ao tentar fazer o login - {e}")

    return render(request, 'login.html', {'form': form})


def logout_system(request):
    logout(request)
    return redirect('user:initial_page')
