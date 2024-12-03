class Propriedade:
    def __init__(self, id, nome, cidade):
        self.id = id
        self.nome = nome
        self.cidade = cidade
    def __repr__(self) -> str:
        return f"<Propriedade: {self.id}, {self.nome}, {self.cidade}>"

    def getNome(self):
        return self.nome

    def toJson(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cidade': self.cidade
        }
