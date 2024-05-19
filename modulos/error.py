class ErrorPrograma(Exception):
    def __init__(self, mensaje):
        """
            Clase que crea un error personalizado para imprimir en el main
        Args:
            mensaje (String): Mensaje que devolvera el codigo al capturarlo en el exception
        """        
        super().__init__(mensaje)
        self.mensaje = mensaje

    def __str__(self):
        return self.mensaje

 