

# References:
# Baty 2024


import pypinnch as pn



#########################################
# Problem Parameters


labels = 'x; u'


class Parameters(pn.Parameters):

    def __init__(self):
        super().__init__()

        self.c = 1.0
        # typ. range 0.1 ... 1.1
        self.mu = 0.15
        # Reynolds number R_e = c/mu
        # stiff when R_e >> 1

        self.ranges = {
            'x': (0.0, 1.0),
            # upper bound 0.6 ok if 1.0 > mu > 0.15,
            # after that solution becomes singular near x=1.0,
            # as can be seen from u_ref
            'u': (0.0, 0.6),
        }


#########################################
# Constraints


interior = pn.source.Box90(
    proportions=lambda p: [p.extent('x')],
    origin=lambda p: [p.min('x')],
    mode='pseudo',
)

left = pn.source.Box90(
    proportions=lambda p: [pn.ConstantDim(p.min('x'))],
    origin=lambda p: [None],
    mode='pseudo',
)

right = pn.source.Box90(
    proportions=lambda p: [pn.ConstantDim(p.max('x'))],
    origin=lambda p: [None],
    mode='pseudo',
)



def residual(problem, hub):
    c = problem.p.c
    mu = problem.p.mu
    u_x, u_xx = problem.get('u_x, u_x_x', hub)
    return pn.eq(
        LHS=-mu*u_xx + c*u_x,
        RHS=1.0,
    )

def bc_dirichlet(problem, hub):
    u = problem.get('u', hub)
    return pn.eq(
        LHS=u,
    )

constraint1 = pn.constraint.Constraint(
    label='u_Poisson',
    source=interior,
    residual=residual,
)

constraint2 = pn.constraint.Constraint(
    label='bc_left',
    source=left,
    residual=bc_dirichlet,
)

constraint3 = pn.constraint.Constraint(
    label='bc_right',
    source=right,
    residual=bc_dirichlet,
)

constraints = [constraint1, constraint2, constraint3]


#########################################


solutions = {
    "x; u": pn.Solution(
        every=1,
        methods={
            'u': 'direct',
        }
    ),
}


#########################################
# References


# Warning: this solution assumes c = 1.0
def u_ref(X, problem):
    mu = problem.p.mu
    x = problem.get('x', X=X)
    a = pn.exp((x-1.0)/mu)
    b = pn.constant_like(a, pn.scalar.exp(-1.0/mu))
    c = pn.constant_like(a, 1.0)
    subexp = (a - b)/(c - b)
    return x - subexp

references = {
    "x; u": pn.Reference(methods=u_ref)
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

