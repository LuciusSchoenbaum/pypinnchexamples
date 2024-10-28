

import pypinnch as pn

from engine1 import engine
from problem1 import problem
from models1 import models

# dryrun = True
dryrun = False
stride = 1
early_nstride = None

topline = pn.TopLine(
    dryrun=dryrun,
    stride=1,
    early_nstride=early_nstride,
)

seed = 123
clean=True
backend=pn.cuda_if_available()
# precision=32
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

