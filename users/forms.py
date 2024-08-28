from django import forms
from django.contrib.auth import get_user_model


# получение текущей модели пользователя
User = get_user_model()


# создание формы регистрации пользователя
class UserRegistrationForm(forms.ModelForm):
    # создание дополнительного поля пароля для повторного ввода при регистрации
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def clean_password2(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['password'] != cleaned_data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cleaned_data['password2']

    class Meta:
        model = User
        fields = ('username', 'password',
                  'first_name', 'last_name', 'email',
                  'phone', 'city')
