from django.shortcuts import render, get_object_or_404, redirect
from .models import Produto, Carrinho, ItemCarrinho, Pedido, Categoria, Cliente
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginClienteForm, CadastroClienteForm
from django.contrib import messages


@login_required(login_url='/login/') 
def index(request):
    return render(request, 'base.html')

# Página de login do cliente
def login_cliente(request):
    if request.user.is_authenticated:
        return redirect('cardapio')  # Redireciona para o cardápio se já estiver logado

    if request.method == 'POST':
        form = LoginClienteForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cardapio')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = LoginClienteForm()

    return render(request, 'login_cliente.html', {'form': form})

# Página de cadastro do cliente

def cadastro_cliente(request):
    if request.user.is_authenticated:
        return redirect('cardapio')  # Se já estiver logado, redireciona para o cardápio

    if request.method == 'POST':
        form = CadastroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()  # Salva o usuário e o cliente
            login(request, user)  # Loga automaticamente após cadastro
            return redirect('cardapio')  # Redireciona para a página do cardápio ou outra página
    else:
        form = CadastroClienteForm()

    return render(request, 'cadastro_cliente.html', {'form': form})

# Página de logout do cliente
def logout_cliente(request):
    logout(request)  # Faz o logout
    return redirect('login_cliente')  # Redireciona para a página de login após logout

# Página do cardápio
@login_required
def cardapio(request):
    categorias = Categoria.objects.all()  # Buscar todas as categorias
    return render(request, 'cardapio.html', {'categorias': categorias})

# Adicionar um produto ao carrinho
@login_required
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    # Verificar se o usuário tem um Cliente associado
    if not hasattr(request.user, 'cliente'):
        # Se o usuário não tem cliente, criar um novo Cliente automaticamente
        cliente = Cliente.objects.create(user=request.user, endereco='', telefone='')  # Ajuste conforme necessidade
    else:
        cliente = request.user.cliente

    # Criar ou obter o carrinho do cliente
    carrinho, created = Carrinho.objects.get_or_create(cliente=cliente)

    # Verificar se o produto já foi adicionado ao carrinho para evitar duplicação
    if not carrinho.itens.filter(id=produto.id).exists():
        # Adicionar o produto ao carrinho
        carrinho.itens.add(produto)

    return redirect('carrinho')  # Redireciona para o carrinho

# Excluir um item do carrinho
@login_required
def excluir_item_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)

    # Garantir que o item esteja no carrinho do usuário
    if item.carrinho.cliente == request.user.cliente:
        item.delete()

    return redirect('carrinho')  # Redireciona para o carrinho após excluir o item


# Finalizar o pedido
@login_required
def finalizar_pedido(request):
    carrinho = get_object_or_404(Carrinho, cliente=request.user.cliente)

    if carrinho.itens.count() == 0:
        return redirect('cardapio')  # Redireciona para o cardápio se o carrinho estiver vazio

    # Criar pedido
    pedido = Pedido.objects.create(
        cliente=carrinho.cliente,
        endereco_entrega=carrinho.cliente.endereco,
        telefone_entrega=carrinho.cliente.telefone,
    )

    # Adicionar itens ao pedido
    for item in carrinho.itens.all():
        pedido.itens.add(item)

    # Limpar carrinho após o pedido
    carrinho.itens.clear()

    # Simulando o pagamento
    pedido.finalizar()

    return render(request, 'pedido_finalizado.html', {'pedido': pedido})

def carrinho(request):
    carrinho = get_object_or_404(Carrinho, cliente=request.user.cliente)
    return render(request, 'carrinho.html', {'carrinho': carrinho})