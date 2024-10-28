

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
    stride=stride,
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


def config_bc_dir(e):
    e.problem.p.bc_case = 'dirichlet'

def config_bc_neu(e):
    e.problem.p.bc_case = 'neumann'

def config_bc_mix(e):
    e.problem.p.bc_case = 'mixed dirichlet-neumann'

def config_1(e):
    e.problem.p.case = '1'
    # awk
    e.problem.p.ranges['u'] = (-1.0, 1.0)

def config_a(e):
    e.problem.p.case = 'a'
    # awk
    e.problem.p.ranges['u'] = (0.0, pn.exp1)

def config_b(e):
    e.problem.p.case = 'b'
    # awk
    e.problem.p.ranges['u'] = (1.0, pn.exp1+0.5)

def config_c(e):
    e.problem.p.case = 'c'
    # awk
    # todo
    e.problem.p.ranges['u'] = (0.0, 1.0)

def config_d(e):
    e.problem.p.case = 'd'
    # awk
    # todo
    e.problem.p.ranges['u'] = (1.0, pn.scalar.exp(2))

def config_e(e):
    e.problem.p.case = 'e'
    # awk
    # todo
    e.problem.p.ranges['u'] = (1.0, pn.exp1+pn.scalar.sinh(1))



if __name__ == '__main__':

    # test
    config_a(engine)
    config_bc_dir(engine)
    engine.start()

