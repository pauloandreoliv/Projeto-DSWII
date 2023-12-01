from Lista import Lista
from Produtos import Produtos


lista = Lista()
p1 = Produtos('----', 20)
lista.produtos.append(p1)

for item in lista.produtos:
    print(item.nome, item.preco)
