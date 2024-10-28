

# References:
# Baty 2024


import pypinnch as pn



#########################################
# Problem Parameters


labels = 'x; u, mu'
mu_true_value = 0.15


class Parameters(pn.Parameters):

    def __init__(self):
        super().__init__()

        self.c = 1.0

        self.ranges = {
            'x': (0.0, 1.0),
            # upper bound 0.6 ok if 1.0 > mu > 0.15,
            # after that solution becomes singular near x=1.0, see u_ref
            'u': (0.0, 0.6),
            'mu': (0.0, 1.0),
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
    mu = problem.get('mu', hub)
    u_x, u_xx = problem.get('u_x, u_x_x', hub)
    return pn.eq(
        LHS=-mu*u_xx + c*u_x,
        RHS=1.0,
    )

def residual2(problem, hub):
    mu_x = problem.get('mu_x', hub)
    return pn.eq(
        LHS=mu_x,
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

constraint4 = pn.constraint.Constraint(
    label='data1',
    source=pn.source.DataSet(labels = 'x; u', filename="noisydata.dat"),
)

constraint5 = pn.constraint.Constraint(
    label='param1',
    source=interior,
    residual=residual2,
)

constraints = [
    constraint1,
    constraint2,
    constraint3,
    constraint4,
    constraint5,
]


#########################################


solutions = {
    "x; u, mu": pn.Solution(
        every=1,
        methods={
            'u': 'direct',
            'mu': 'direct',
        }
    ),
}


#########################################
# References


# Warning: this solution assumes c = 1.0
def u_ref(X, problem):
    mu = mu_true_value
    x = problem.get('x', X=X)
    a = pn.exp((x-1.0)/mu)
    b = pn.constant_like(a, pn.scalar.exp(-1.0/mu))
    c = pn.constant_like(a, 1.0)
    subexp = (a - b)/(c - b)
    return x - subexp

def mu_ref(X, problem):
    return problem.get_constant(mu_true_value, X=X)


references = {
    "x; u, mu": pn.Reference(
        methods={
            'u': u_ref,
            'mu': mu_ref,
        }
    ),
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

