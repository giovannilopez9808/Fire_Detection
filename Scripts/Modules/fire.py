from datetime import timedelta
from .firms import FIRMSData
from .citys import CityList
from os.path import join
from numpy import (
    arange,
    array,
    zeros,
    round,
    size,
    sum,
)


class FireCount:
    def __init__(
        self,
        only_nominal_data: bool,
        color: str
    ) -> None:
        """
        Conteo de los datos de FIRMS en una localización fijada.
        Parameters
        ----------
        # Inputs
        + City_name -> Nombre de la ciudad donde se cargaran los parametros
        + select_nominal_data -> valor para seleccionar solamente los
                                datos de tipo nominal
        + color -> color del numero por imprimir en las graficas
        ---------
        """
        self.lon_division = None
        self.lat_division = None
        self.lon_n = None
        self.lat_n = None
        self._get_city_parameters()
        self.FIRMS_data = FIRMSData(
            params=self.params,
            only_nominal_data=only_nominal_data
        )
        self.color = color

    def _get_city_parameters(
        self,
    ) -> None:
        """
        Selecciona los parametros dependiendo del nombre de la ciudad
        """
        city_parameters = CityList()
        self.params = city_parameters.parameters

    def _create_grids(
        self
    ) -> None:
        """
        Funcion que crea las grillas de busqueda y realiza la
        transformacion para el espacio de la imagen
        """
        self.lon_division, self.lon_n = self._delimiter_grids(
            self.params["lon"],
            self.params["delta"]
        )
        self.lat_division, self.lat_n = self._delimiter_grids(
            self.params["lat"],
            self.params["delta"]
        )

    def _delimiter_grids(
        self,
        pos_points: list,
        delta: float = 0.25
    ) -> tuple:
        """
        Funcion para obtener el numero de grillas
        """
        pos = round(
            arange(
                pos_points[0],
                pos_points[1]+delta,
                delta
            ),
            3
        )
        data_size = size(
            pos
        )
        return pos, data_size

    def run(
        self
    ) -> None:
        """
        Funcion que realiza el algoritmo de conteo en los distintos archivos
        e FIRMS y dos formatos de archivos

        NI.csv -----> Conteo de los incencos para distintas fechas
        """
        print(
            "Realizando conteo de incendios"
        )
        # Archivo NI
        filename = join(
            "../data",
            "NI.csv",
        )
        results_file = open(
            filename,
            "w"
        )
        results_file.write(
            "Dates,NI",
        )
        dates = self._get_dates()
        data = self.FIRMS_data.data
        date_i = dates[0].date()
        date_f = dates[-1].date()
        print(
            f"Inicio del conteo del día {date_i} al {date_f}"
        )
        for date in dates:
            # Seleccion de los datos por dia
            daily_data = data[data.index == date]
            # Conteo de los incendios para cada grilla
            count = self._count_fire(
                daily_data
            )
            # Conteo de los incendios para todo el dia
            daily_sum = sum(count)
            print(date, daily_sum)
            # Escritura de los resultados
            results_file.write(
                "{},{}\n".format(
                    date.date(),
                    daily_sum
                )
            )
        results_file.close()

    def _count_fire(
        self,
        data: array
    ) -> array:
        """
        Algoritmo para el conteo de los incendios en cada grilla
        """
        # Inicializacion del conteo
        count = zeros(
            [
                self.lon_n,
                self.lat_n
            ],
            dtype=int,
        )
        # Longitud de los datos
        for lon_i in range(self.lon_n-1):
            # Limites de la grilla en la longitud
            lon_j = [
                self.lon_division[lon_i],
                self.lon_division[lon_i+1]
            ]
            for lat_i in range(self.lat_n-1):
                # Limites de la grilla en la latitud
                lat_j = [
                    self.lat_division[lat_i],
                    self.lat_division[lat_i+1]
                ]
                # Localizacion de los datos a partir de su longitud
                data_loc = self.FIRMS_data.get_data_from_positions(
                    data,
                    "longitude",
                    lon_j
                )
                # Localizacion de los datos a partir de su latitud
                data_loc = self.FIRMS_data.get_data_from_positions(
                    data_loc,
                    "latitude",
                    lat_j
                )
                count[lon_i, lat_i] = data_loc["latitude"].count()
        return count

    def _get_dates(self) -> list:
        """
        Obtiene las fechas consecutivas en el periodo
        """
        days = (
            self.params["day final"] - self.params["day initial"]
        ).days
        dates = list()
        for day in range(days+1):
            date = self.params["day initial"]+timedelta(days=day)
            dates.append(date)
        return dates
