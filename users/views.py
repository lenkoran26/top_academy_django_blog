from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash
from myblog.settings import LOGIN_REDIRECT_URL
from .forms import UserRegistrationForm, CustomPasswordChangeForm


User = get_user_model()


def register(request):
    #если нажали кнопку регистрация (метод Post)
    if request.method == "POST":
        #создаем объект формы с данными из запроса
        user_form = UserRegistrationForm(request.POST)
        #валидация формы (правильность введенных данных)
        if user_form.is_valid():
            # создание объекта с полями формы (без сохранения в БД)
            new_user = user_form.save(commit=False)
            # хэширование пароля пользователя
            new_user.set_password(user_form.cleaned_data['password'])
            # сохранение пользователя в БД
            new_user.save()
            context = {'title': 'Успешная регистрация', 'new_user': new_user}
            return render(request, template_name='users/register_done.html', context=context)

    # метод GET - отрисовка страницы регистрации
    user_form = UserRegistrationForm()
    context = {'title': 'Регистрация', 'register_form': user_form}
    return render(request, template_name='users/register.html', context=context)


def log_in(request):
    # создание формы аутентификации
    form = AuthenticationForm(request, request.POST)
    # проверка формы
    if form.is_valid():
        # получение логина и пароля из формы
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # аутентификация пользователя (проверка наличия поль-ля и пароля)
        user = authenticate(username=username, password=password)
        if user:
            # авторизация пользователя (получение прав доступа)
            login(request, user)
            # получение дальнейшего маршрута после авторизации (next - путь, откуда пришел пользователь)
            url = request.GET.get('next', LOGIN_REDIRECT_URL)
            return redirect(url)
    context = {'form': form}
    return render(request, template_name='users/login.html', context=context)


@login_required
def log_out(request):
    logout(request)
    return redirect('blog:index')


@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.user != user:
       raise PermissionDenied()

    context = {'user': user, 'title': 'Информация о профиле'}
    return render(request, template_name='users/profile.html', context=context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.POST)

        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password_1']

            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('blog:index')

            else:
                form.add_error('old_password', 'Старый пароль неверный')
                return redirect('users:change_password')

        return redirect('users:change_password')

    else:
        form = CustomPasswordChangeForm()
        context = {'title': 'Сменить пароль', 'form': form}
        return render(request, template_name='users/change_password.html', context=context)
