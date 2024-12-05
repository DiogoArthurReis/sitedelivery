# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Cliente

class LoginClienteForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# Formulário de cadastro
class CadastroClienteForm(forms.Form):
    nome_completo = forms.CharField(max_length=100, label='Nome Completo', widget=forms.TextInput(attrs={'placeholder': 'Digite seu nome completo'}))
    username = forms.CharField(max_length=30, label='Usuário', widget=forms.TextInput(attrs={'placeholder': 'Escolha um nome de usuário'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}))
    telefone = forms.CharField(max_length=15, label='Telefone', widget=forms.TextInput(attrs={'placeholder': 'Digite seu telefone'}))
    rua = forms.CharField(max_length=255, label='Rua', widget=forms.TextInput(attrs={'placeholder': 'Digite sua rua'}))
    numero = forms.CharField(max_length=20, label='Número', widget=forms.TextInput(attrs={'placeholder': 'Digite o número'}))
    bairro = forms.CharField(max_length=100, label='Bairro', widget=forms.TextInput(attrs={'placeholder': 'Digite seu bairro'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}), label='Senha')
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirme sua senha'}), label='Confirmar Senha')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Esse nome de usuário já está em uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Esse e-mail já está em uso.')
        return email

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if len(senha) < 8:
            raise ValidationError('A senha deve ter pelo menos 8 caracteres.')
        return senha

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')
        if senha != confirmar_senha:
            raise ValidationError('As senhas não coincidem.')
        return confirmar_senha

    def save(self):
        nome_completo = self.cleaned_data.get('nome_completo')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        senha = self.cleaned_data.get('senha')
        telefone = self.cleaned_data.get('telefone')
        rua = self.cleaned_data.get('rua')
        numero = self.cleaned_data.get('numero')
        bairro = self.cleaned_data.get('bairro')

        # Criar o usuário
        user = User.objects.create_user(username=username, email=email, password=senha)

        # Criar o cliente
        cliente = Cliente(user=user, nome_completo=nome_completo, telefone=telefone, rua=rua, numero=numero, bairro=bairro)
        cliente.save()

        return user