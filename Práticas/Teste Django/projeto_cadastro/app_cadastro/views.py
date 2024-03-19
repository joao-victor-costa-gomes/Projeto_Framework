from django.shortcuts import render
from .models import Usuario

def home(request):
    return render(request, "home.html")

def lista_usuarios(request):
    # Salvar os dados da tela para o banco de dados 
    novo_usuario = Usuario()
    novo_usuario.nome = request.POST.get('nome')
    novo_usuario.idade = request.POST.get('idade')
    novo_usuario.save()
    # Exibir todos os usuários cadastrados em uma nova página 
    usuarios = {
        'usuarios': Usuario.objects.all()
    }
    # Retornar os dados para a página da lista de usuários 
    return render(request, "usuarios.html", usuarios)