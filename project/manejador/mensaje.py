class Mensaje:
    def __init__(self, estacionamiento=None, puerta=None, placa=None, tipo=None):
        self.estacionamiento = estacionamiento
        self.puerta = puerta
        self.placa = placa
        self.tipo = tipo
        
    def toJSON(self):
        return self.__dict__
    