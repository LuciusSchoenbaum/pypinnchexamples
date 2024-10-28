

import pypinnch as pn

from engine1 import engine
from problem1 import problem
from models1 import models

# dryrun = True
dryrun = False

topline = pn.TopLine(
    dryrun=dryrun,
    stride=1,
    early_nstride=None,
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


def config_adam(e):
    for d in e.drivers:
        # todo ack - mess, fix
        d.phases[0].strategies.optimizer.init_kit.max_iterations = 10000
        # todo old code, fix
        d.phases[0].strategies.optimizer.id = 0

def config_LBFGS(e):
    for d in e.drivers:
        # todo ack - mess, fix
        d.phases[0].strategies.optimizer.init_kit.max_iterations = 10
        # todo old code, fix
        d.phases[0].strategies.optimizer.id = 1


if __name__ == '__main__':

    engine.start()

