

# References:
# Nishikawa 2023
# Baty 2024


import pypinnch as pn


def u_exact(x, y, case):
    if case == '1':
        return x*x-y*y
    if case == 'a':
        return pn.exp(x*y)
    if case == 'b':
        k = 1.0
        return pn.exp(k*x)*pn.sin(k*y) + 0.25*(x*x + y*y)
    if case == 'c':
        return pn.sinh(x)
    if case == 'd':
        return pn.exp(x*x+y*y)
    if case == 'e':
        return pn.exp(x*y) + pn.sinh(x)
    else:
        raise NotImplementedError

def u_x_exact(x, y, case):
    if case == '1':
        return 2*x
    if case == 'a':
        return y*pn.exp(x*y)
    elif case == 'b':
        k = 1.0
        return k*pn.exp(k*x)*pn.sin(k*y) + 0.25*2.0*x
    elif case == 'c':
        return pn.cosh(x)
    elif case == 'd':
        return 2.0*x*pn.exp(x*x+y*y)
    elif case == 'e':
        return y*pn.exp(x*y) + pn.cosh(x)
    else:
        raise NotImplementedError

def u_y_exact(x, y, case):
    if case == '1':
        return 2*y
    if case == 'a':
        return x*pn.exp(x*y)
    elif case == 'b':
        k = 1.0
        return k*pn.exp(k*x)*pn.cos(k*y) + 0.25*2.0*y
    elif case == 'c':
        return pn.constant_like(x, 0.0)
    elif case == 'd':
        return 2.0*y*pn.exp(x*x+y*y)
    elif case == 'e':
        return x*pn.exp(x*y)
    else:
        raise NotImplementedError

def f_source(x, y, case):
    if case == '1':
        return pn.constant_like(x, 0.0)
    if case == 'a':
        return pn.exp(x*y)*(x*x + y*y)
    elif case == 'b':
        return pn.constant_like(x, 1.0)
    elif case == 'c':
        return pn.sinh(x)
    elif case == 'd':
        return 4.0*(x*x + y*y + 1.0)*pn.exp(x*x+y*y)
    elif case == 'e':
        return pn.exp(x*y)*(x*x + y*y) + pn.sinh(x)
    else:
        raise NotImplementedError


#########################################
# Problem Parameters


labels = 'x, y; u'



class Parameters(pn.Parameters):

    def __init__(self):
        super().__init__()

        L = 1.0
        self.case = 'undefined'
        self.bc_case = 'undefined'
        self.ranges = {
            'x': (0.0, L),
            'y': (0.0, L),
            'u': None,
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


#########################################
# Constraints


def residual(problem, hub):
    case = problem.p.case
    x, y = problem.get('x, y', hub)
    u_xx, u_yy = problem.get('u_x_x, u_y_y', hub)
    return pn.eq(
        LHS=u_xx + u_yy,
        RHS=f_source(x, y, case),
    )

def dirichlet_bc(problem, hub):
    case = problem.p.case
    u, x, y = problem.get('u, x, y', hub)
    return pn.eq(
        LHS=u,
        RHS=u_exact(x, y, case),
    )

def neumann_bc_vertical_bdy(problem, hub):
    case = problem.p.case
    u_n, x, y = problem.get('u_x, x, y', hub)
    return pn.eq(
        LHS=u_n,
        RHS=u_x_exact(x, y, case),
    )

def neumann_bc_horizontal_bdy(problem, hub):
    case = problem.p.case
    u_n, x, y = problem.get('u_y, x, y', hub)
    return pn.eq(
        LHS=u_n,
        RHS=u_y_exact(x, y, case),
    )

def bc_left(problem, hub):
    bc_case = problem.p.bc_case
    if bc_case == 'dirichlet':
        return dirichlet_bc(problem, hub)
    elif bc_case == 'neumann':
        return neumann_bc_vertical_bdy(problem, hub)
    elif bc_case == 'mixed dirichlet-neumann':
        return dirichlet_bc(problem, hub)
    else:
        raise ValueError

def bc_right(problem, hub):
    bc_case = problem.p.bc_case
    if bc_case == 'dirichlet':
        return dirichlet_bc(problem, hub)
    elif bc_case == 'neumann':
        return neumann_bc_vertical_bdy(problem, hub)
    elif bc_case == 'mixed dirichlet-neumann':
        return neumann_bc_vertical_bdy(problem, hub)
    else:
        raise ValueError

def bc_top(problem, hub):
    bc_case = problem.p.bc_case
    if bc_case == 'dirichlet':
        return dirichlet_bc(problem, hub)
    elif bc_case == 'neumann':
        return neumann_bc_horizontal_bdy(problem, hub)
    elif bc_case == 'mixed dirichlet-neumann':
        return neumann_bc_horizontal_bdy(problem, hub)
    else:
        raise ValueError

def bc_bottom(problem, hub):
    bc_case = problem.p.bc_case
    if bc_case == 'dirichlet':
        return dirichlet_bc(problem, hub)
    elif bc_case == 'neumann':
        return neumann_bc_horizontal_bdy(problem, hub)
    elif bc_case == 'mixed dirichlet-neumann':
        return dirichlet_bc(problem, hub)
    else:
        raise ValueError


constraints = {
    'u_Poisson': pn.constraint.Constraint(
        source=interior,
        residual=residual,
    ),
    'bc_left': pn.constraint.Constraint(
        source=left,
        residual=bc_left,
    ),
    'bc_right': pn.constraint.Constraint(
        source=right,
        residual=bc_right,
    ),
    'bc_bottom': pn.constraint.Constraint(
        source=bottom,
        residual=bc_bottom,
    ),
    'bc_top': pn.constraint.Constraint(
        source=top,
        residual=bc_top,
    ),
}


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
    case = problem.p.case
    x, y = problem.get('x, y', X=X)
    return u_exact(x, y, case)

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



