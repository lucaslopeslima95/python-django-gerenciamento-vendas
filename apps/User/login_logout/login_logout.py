from django.contrib.auth import (logout,
                                 login)
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from User.forms import authForm
from User.views import initial_page
from django.contrib import messages

@csrf_protect
def login_system(request):
    """Gerencia o sistema de login do usuário.

    Esta função lida com a lógica de autenticação do usuário. Se o usuário já estiver autenticado,
    redireciona para a página inicial. Caso contrário, trata a requisição de login, verifica as credenciais
    do usuário e realiza o login se as credenciais forem válidas.

    Args:
        request (HttpRequest): A requisição HTTP recebida.

    Returns:
        HttpResponse: A resposta HTTP renderizada como HTML.
    """
    form = authForm()    
    try:
        if request.user.is_authenticated:
            return initial_page(request)
        
        if request.method == "POST":
            form = authForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('user:initial_page')
                else:
                    messages.warning(request, "Usuario ou Senha Errados.")
            else:
                messages.warning(request, "Credenciais inválidas.")
    except Exception as e :
        print(f"Exceção ao tentar fazer o login - {e}")
        
    return render(request, 'login.html', {'form': form})



def logout_system(request):
    """_summary_

    Args:
        request (_type_): Requisição do Usuario
        para realizar o logout do user logado
    Returns:
        Redirect: Vai para a pagina inicial, login da aplicação
    """
    logout(request)
    return redirect('user:initial_page')