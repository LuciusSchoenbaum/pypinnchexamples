

import pypinnch as pn


def u_exact(x, y):
    return (1+x*x)*(1+y*y)

def u_x_exact(x, y):
    return 2.0*x*(1+y*y)

def u_y_exact(x, y):
    return 2.0*y*(1+x*x)


#########################################
# Problem Parameters


labels = 'x, y; u'

class Parameters(pn.Parameters):

    def __init__(self):
        super().__init__()

        self.alpha = 2.0
        self.beta = 2.0

        self.ranges = {
            'x': (0.0, 2.0),
            'y': (-1.0, 1.0),
            'u': (0.0, 10.0),
        }


#########################################
# Sources


interior = pn.source.Box90(
    proportions=lambda p: [p.extent('x'), p.extent('y')],
    origin=lambda p: [p.min('x'), p.min('y')],
    mode='pseudo',
)

left = pn.source.Box90(
    proportions=lambda p: [pn.ConstantDim(p.min('x')), p.extent('y')],
    origin=lambda p: [None, p.min('y')],
    mode='pseudo',
)

right = pn.source.Box90(
    proportions=lambda p: [pn.ConstantDim(p.max('x')), p.extent('y')],
    origin=lambda p: [None, p.min('y')],
    mode='pseudo',
)

bottom = pn.source.Box90(
    proportions=lambda p: [p.extent('x'), pn.ConstantDim(p.min('y'))],
    origin=lambda p: [p.min('x'), None],
    mode='pseudo',
)

top = pn.source.Box90(
    proportions=lambda p: [p.extent('x'), pn.ConstantDim(p.max('y'))],
    origin=lambda p: [p.min('x'), None],
    mode='pseudo',
)

domain = interior

leftright = pn.source.Union()
leftright += left
leftright += right
bottop = pn.source.Union()
bottop += bottom
bottop += top


#########################################
# Constraints


def lane_emden_equation(problem, hub):
    alpha = problem.p.alpha
    beta = problem.p.beta
    x, y, u_x, u_y, u_xx, u_yy = problem.get('x, y, u_x, u_y, u_x_x, u_y_y', hub)
    f = 6.0*(2.0+x*x+y*y)
    return pn.eq(
        LHS=x*y*(u_xx + u_yy) + alpha*y*u_x + beta*x*u_y,
        RHS=x*y*f,
    )


def bc_dirichlet(problem, hub):
    x, y, u = problem.get('x, y, u', hub)
    return pn.eq(
        LHS=u,
        RHS=u_exact(x, y),
    )

def bc_neumann_leftright(problem, hub):
    x, y, u_y = problem.get('x, y, u_y', hub)
    return pn.eq(
        LHS=u_y,
        RHS=u_y_exact(x, y)
    )

def bc_neumann_bottop(problem, hub):
    x, y, u_x = problem.get('x, y, u_x', hub)
    return pn.eq(
        LHS=u_x,
        RHS=u_x_exact(x, y)
    )


constraint1 = pn.constraint.Constraint(
    label='u_pde',
    source=domain,
    residual=lane_emden_equation,
)

constraint2 = pn.constraint.Constraint(
    label='bc_dir_lr',
    source=leftright,
    residual=bc_dirichlet,
)

constraint3 = pn.constraint.Constraint(
    label='bc_neu_lr',
    source=leftright,
    residual=bc_neumann_leftright,
)

constraint4 = pn.constraint.Constraint(
    label='bc_neu_tb',
    source=bottop,
    residual=bc_neumann_bottop,
)

constraints = [constraint1, constraint2, constraint3, constraint4]
# todo test variations in BCs following Baty against acc/ttx

#########################################


solutions = {
    "x, y; u": pn.Solution(
        every=1,
        methods={
            'u': 'direct',
        }
    ),
}


#########################################
# References


def u_ref(X, problem):
    x, y = problem.get('x, y', X=X)
    return u_exact(x, y)

references = {
    "x, y; u": pn.Reference(methods=u_ref)
}


#########################################


problem = pn.Problem(
    labels=labels,
    Parameters=Parameters,
    constraints=constraints,
    solutions=solutions,
    references=references,
    file=__file__,
)

