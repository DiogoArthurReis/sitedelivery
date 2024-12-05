# admin.py
from django.contrib import admin
from .models import Categoria, Produto, Carrinho, ItemCarrinho, Pedido, Entregador, Cliente

class ItemCarrinhoInline(admin.TabularInline):
    model = ItemCarrinho
    extra = 0

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'status', 'criado_em', 'atualizado_em')
    list_filter = ('status', 'cliente')
    search_fields = ('cliente__user__username',)
    inlines = [ItemCarrinhoInline]  # Exibir os itens do pedido diretamente na tela de pedidos

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'descricao')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'telefone', 'rua', 'numero', 'bairro')  # Adapte aqui
    search_fields = ('nome_completo', 'telefone', 'bairro')  # Adapte conforme necessário
    list_filter = ('bairro',)
    
class EntregadorAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefone')
    search_fields = ('user__username',)

# Usando o decorador para registrar o Produto com a classe ProdutoAdmin
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'descricao')
    list_filter = ('categoria',)
    search_fields = ('nome', 'descricao')

# Registro dos modelos no painel administrativo
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Carrinho)
admin.site.register(ItemCarrinho)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Entregador, EntregadorAdmin)
admin.site.register(Categoria)
