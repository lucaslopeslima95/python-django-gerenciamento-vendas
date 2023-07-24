from sqlite3 import IntegrityError

from django.contrib import messages
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import registerCategoryForm
from .models import Category


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def main_menu_category(request):
    try:
        categorys = None
        if 'filter' in request.session:
            filter = request.session['filter']
        else:
            filter = None
        filter = request.session['filter']
        if filter:
            categorys = Category.objects.filter(
                name__startswith=filter).order_by('name')
            request.session['filter'] = ""
        else:
            categorys = Category.objects.all().order_by('name')
    except (Category.DoesNotExist, Exception) as e:
        print(f"Exceção listar as categorias no menu principal - {e}")
    return render(request, 'category/main_menu_category.html',
                  {'categorys': categorys})


@user_passes_test(lambda user: user.is_superuser or
                  user.is_staff, login_url='user:page_not_found')
@login_required(login_url="login_system")
def save_category(request):
    try:
        if request.method == "POST":
            form = registerCategoryForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name'].capitalize()
                description = form.cleaned_data['description']
                Category.objects.create(name=name,
                                        description=description).save()
                messages.success(request, "Salvo com sucesso")
            else:
                messages.warning(request, "Dados Inválidos")
            return redirect('category:main_menu_category')
        else:
            form = registerCategoryForm()
    except (Exception, IntegrityError) as e:
        if 'name' in e:
            messages.warning(request, "Erro ao Salvar categoria")
        else:
            messages.warning(request, "Esse nome de categoria ja existe")
    return render(request, 'category/save_category.html', {'form': form})


@user_passes_test(lambda user: user.is_superuser or user.is_staff,
                  login_url='user:page_not_found')
@login_required(login_url="login_system")
def update_category(request, id):
    category_selected = Category.objects.get(id=id)
    form = registerCategoryForm(request.POST or None,
                                instance=category_selected)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name'].capitalize()
            description = form.cleaned_data['description']
            Category.objects.filter(id=id).update(name=name,description=description)
            messages.success(request, "Atualizado com sucesso")
        else:
            messages.warning(request, "Dados Invalido")
            return redirect('category:main_menu_category')
    return render(request, 'category/update_category.html', {'form': form})
