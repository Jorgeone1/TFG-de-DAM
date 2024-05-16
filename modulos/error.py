class ErrorPrograma(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje

    def __str__(self):
        return self.mensaje

 