
# Description: Helmholtz equation 2d case
# with analytic solution.


import pypinnch as pn


def u_exact(x, z, a_, nu_, L):
    u = pn.zeros_like(x)
    for k in range(1,4):
        A = a_[k]*pn.exp(-nu_[k]*z)
        u += A*pn.cos(k*pn.pi/L*x)
    return u

#########################################
# Problem Parameters


labels = 'x, z; u'

class Parameters(pn.Parameters):
    def __init__(self):
        super().__init__()

        self.L = 3.0
        L = self.L
        self.ranges = {
            'x': (-L/2.0, L/2.0),
            # it is interesting to look at the domain z in -L/2 to 0.0
            'z': (0.0, L),
            'u': (-0.51, 2.1),
        }

        self.c = 0.8

        # integers (a1, a2, a3)
        a1 = 1.0
        a2 = 0.0
        a3 = 1.0
        # ...also try (1, 0, -1)
        self.a_ = [0.0, a1, a2, a3]
        self.nu_ = [0.0]
        cc = self.c*self.c
        for k in range(1, 4):
            a = k*pn.pi/L
            aa = a*a
            self.nu_.append(pn.scalar.sqrt(aa - cc))


#########################################
# Constraints


base_domain = pn.source.Box90(
    proportions=lambda p: [p.extent('x'), p.extent('z')],
    origin=lambda p: [p.min('x'), p.min('z')],
    mode='pseudo',
)

left_bdy = pn.source.Box90(
    proportions=lambda p: [pn.ConstantDim(p.min('x')), p.extent('z')],
    origin=lambda p: [p.min('x'), p.min('z')],
    mode='pseudo',
)
right_bdy = pn.source.Box90(
    proportions=lambda p: [pn.ConstantDim(p.max('x')), p.extent('z')],
    origin=lambda p: [p.max('x'), p.min('z')],
    mode='pseudo',
)
top_bdy = pn.source.Box90(
    proportions=lambda p: [p.extent('x'), pn.ConstantDim(p.max('z'))],
    origin=lambda p: [p.min('x'), p.max('z')],
    mode='pseudo',
)
bottom_bdy = pn.source.Box90(
    proportions=lambda p: [p.extent('x'), pn.ConstantDim(p.min('z'))],
    origin=lambda p: [p.min('x'), p.min('z')],
    mode='pseudo',
)

def residual(problem, hub):
    c = problem.p.c
    cc = c*c
    x, z, u = problem.get('x, z, u', hub)
    u_xx, u_zz = problem.get('u_x_x, u_z_z', hub)
    return pn.eq(
        LHS=u_xx + u_zz + cc*u,
        RHS=0.0,
    )

def bc_residual(problem, hub):
    a_ = problem.p.a_
    nu_ = problem.p.nu_
    L = problem.p.L
    x, z, u = problem.get('x, z, u', hub)
    return pn.eq(
        LHS=u,
        RHS=u_exact(x, z, a_, nu_, L)
    )


constraints = {
    'u_Helmholtz': pn.Constraint(
        source=base_domain,
        residual=residual,
    ),
    'u_bc_left': pn.Constraint(
        source=left_bdy,
        residual=bc_residual,
    ),
    'u_bc_rt': pn.Constraint(
        source=right_bdy,
        residual=bc_residual,
    ),
    'u_bc_top': pn.Constraint(
        source=top_bdy,
        residual=bc_residual,
    ),
    'u_bc_bot': pn.Constraint(
        source=bottom_bdy,
        residual=bc_residual,
    ),
}



#########################################
# Solutions


solutions = {
    'x, z; u': pn.Solution(
        every=1,
        methods={
            'u': 'direct',
        }
    ),
}


#########################################
# References


def u_ref(X, problem):
    a_ = problem.p.a_
    nu_ = problem.p.nu_
    L = problem.p.L
    x, z, u = problem.get('x, z, u', X=X)
    return u_exact(x, z, a_, nu_, L)



references = {
    'x, z; u': pn.Reference(methods=u_ref)
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

