class CityList:
    def __init__(
        self,
    ) -> None:
        """
        Contiene los parametros del periodo y zona de análisis de cada región
        ----------------------------
        Inputs:
        + city -> nombre de la ciudad de la cual se cargaran los parámetros

        ----------------------------
        Outouts:
        + self.parameters -> diccionario con los siguientes atributos:
            + day inital -> día inicial del periodo (str)
            + day final -> dia final del periodo (str)
            + lon -> lista con la longitud del área por analizar [float,float]
            + lat -> lista con la latitud del área por analizar [float,float]
            + delta -> divisiones de las grillas del mapa (float)
            + path data -> direccion donde se encuentran los datos
            + file data -> nombre del archivo de datos
            + path graphics -> direccion donde se guardaran las imagenes

        """
        self.parameters = {
            "file data": "data.csv",
            "day initial": "2015-01-01",
            "day final": "2024-12-31",
            "city": "Nuevo_Leon",
            "lon": [-100.75, -99.50],
            "lat": [24.50, 25.50],
            "delta": 0.25,
        }
