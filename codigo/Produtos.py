class Produtos:
    nome: str 
    marca: str
    preco: float
    quantidade: float

    def __init__(self, nome, preco): 
        self.nome = nome
        self.preco= preco
