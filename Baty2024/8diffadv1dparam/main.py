

import pypinnch as pn

from engine1 import engine
from models1 import models
from problem1 import problem


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


def config_mu0(e):
    e.problem.p.mu = 1.0

def config_mu1(e):
    e.problem.p.mu = 0.50

def config_mu2(e):
    e.problem.p.mu = 0.30

def config_mu3(e):
    e.problem.p.mu = 0.15


if __name__ == '__main__':

    engine.start()

