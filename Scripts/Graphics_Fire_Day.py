from Modules.params import get_params
import matplotlib.pyplot as plt
from Modules.functions import (
    obtain_ticks,
    format_data,
)
from os.path import join
from numpy import arange
from pandas import (
    to_datetime,
    read_csv,
)
params = get_params()
params.update({
    "file data": "NI.csv",
    "graphics file": "Fire_Per_Day.png",
    "City name": "Nuevo_Leon_Historic",
    "Days separation": 365,
    "Y limit": 330,
    "Delta y": 30,
    "years": range(
        2012,
        2026,
    )
})
ticks = list(
    to_datetime(f"{year}-01-01")
    for year in params["years"]
)
# Lectura de los datos
filename = join(
    params["path data"],
    params["file data"]
)
data = read_csv(
    filename
)
data = format_data(
    data
)
# Extraccion de las fechas seleccionadas
dates = obtain_ticks(
    data,
    params["Days separation"]
)
plt.subplots(
    figsize=(10, 5)
)
# Ploteo de los datos
plt.plot(
    list(data.index),
    list(data["NI"]),
    color="#9a031e",
    alpha=0.5
)
plt.scatter(
    data.index,
    list(data["NI"]),
    marker=".",
    c="#9a031e",
    alpha=0.5
)
# Limites de las graficas
plt.xlim(
    dates[0],
    dates[-1]
)
plt.ylim(
    0,
    params["Y limit"]
)
# Etiqueta en el eje y
plt.ylabel(
    "Number of active fires per day"
)
# Cambio en las etiquetas de los ejes x y y
plt.xticks(
    ticks,
    params["years"],
    # rotation=45
)
plt.yticks(
    arange(
        0,
        params["Y limit"]+params["Delta y"],
        params["Delta y"]
    )
)
# Creación del grid
plt.grid(
    ls="--",
    color="grey",
    alpha=0.7
)
plt.tight_layout()
# Guardado de la grafica
filename = join(
    params["path graphics"],
    params["graphics file"]
)
plt.savefig(
    filename,
    dpi=400
)
