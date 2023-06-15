import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as pp
import numpy as np
import pandas as pd
import wget
from pathlib import Path
from db import *
from main import ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def load_file(url, username):

    filename = wget.download(url)
    file = Posts(
        post_name = filename,
        username = username
    )
    session.add(file)
    session.commit()


def create_file(file):
    graphpd = pd.read_excel(file)
    graphnp = np.array(graphpd)

    return graphnp


def plotting_graph(array):
    path = Path("static", "myplot.png")
    x = array[:, 0]
    y = array[:, -1]
    pp.plot(x, y)
    pp.title("Таблица")
    pp.xlabel("дата")
    pp.ylabel("значение")
    pp.savefig(path)
    pp.close()
    plot_url = path
    print(path)

    return plot_url

