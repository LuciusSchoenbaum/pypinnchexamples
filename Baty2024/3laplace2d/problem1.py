

import pypinnch as pn



#########################################
# Problem Parameters


labels = 'x, y; u'


class Parameters(pn.Parameters):

    def __init__(self):
        super().__init__()

        L = 1.0
        self.ranges = {
            'x': (-L, L),
            'y': (-L, L),
            'u': (-L*L, L*L),
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

v_bdy = pn.source.Union()
v_bdy += left
v_bdy += right

h_bdy = pn.source.Union()
h_bdy += top
h_bdy += bottom

#########################################
# Constraints

def h_bc(problem, hub):
    u, x = problem.get('u, x', hub)
    return pn.eq(
        LHS=u,
        RHS=x*x - 1.0,
    )

def v_bc(problem, hub):
    u, y = problem.get('u, y', hub)
    return pn.eq(
        LHS=u,
        RHS=1.0 - y*y,
    )

def residual(problem, hub):
    u_xx, u_yy = problem.get('u_x_x, u_y_y', hub)
    return pn.eq(
        LHS=u_xx + u_yy,
    )

constraints = {
    'u_laplacian': pn.Constraint(
        source=domain,
        residual=residual,
    ),
    'bc_v': pn.Constraint(
        source=v_bdy,
        residual=v_bc,
    ),
    'bc_h': pn.Constraint(
        source=h_bdy,
        residual=h_bc,
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
    x, y = problem.get('x, y', X=X)
    return x*x - y*y

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



