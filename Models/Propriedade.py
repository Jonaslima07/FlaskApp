class Propriedade:
    def __init__(self, id, nome, cidade):
        self.id = id
        self.nome = nome
        self.cidade = cidade
    
    def getNome(self):
        return self.nome

    def toJson(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cidade': self.cidade
        }
