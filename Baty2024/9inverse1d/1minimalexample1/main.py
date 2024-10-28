

import pypinnch as pn

from engine1 import engine
from models1 import models
from problem1 import problem


# dryrun = True
dryrun = False

topline = pn.TopLine(
    dryrun=dryrun,
)

seed = 123
clean=True
backend='cpu'
precision=64

background = pn.Background(
    system=None,
    clean=clean,
    seed=seed,
    backend=backend,
    precision=precision,
    file=__file__,
)


engine.set_topline(topline)
engine.set_background(background)
engine.set_problem(problem)
engine.set_models(models)


if __name__ == '__main__':

    engine.start()

