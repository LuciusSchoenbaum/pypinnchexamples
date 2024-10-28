


import pypinnch as pn


def G_exact(R, z, problem):
    """
    The factor G appearing in the
    Grad-Shafranov equation
    for magnetic equilibria of plasma
    in the solar corona.
    """
    case = problem.p.case
    if case == 'Deriazetal':
        f0 = problem.p.f0
        a = problem.p.a
        R0 = problem.p.R0
        G = f0*(R*R + R0*R0)
        return G
    else:
        raise NotImplementedError


def psi_exact(R, z, problem):
    # There are two typos in Baty's paper. Cf. Deriaz et al paper.
    # (1) The boundary z(alpha) = a*R0*sin(alpha), not a*R0
    # (2) The psi here, the numerator in the second term is squared.
    case = problem.p.case
    if case == 'Deriazetal':
        # G = f0*(R*R + R0*R0)
        f0 = problem.p.f0
        a = problem.p.a
        R0 = problem.p.R0
        R02 = R0*R0
        psi = f0*R02/2.0*(a*a - z*z) - f0/8.0*(R*R - R02)*(R*R - R02)
        return psi
    else:
        raise NotImplementedError


#########################################
# Problem Parameters

# spherical variables:
# 'R, phi, z; psi'
# assuming axisymmetric:
labels = 'R, z; psi'



class Parameters(pn.Parameters):

    def __init__(self):
        super().__init__()

        self.f0 = 1.0
        self.a = 0.5
        self.R0 = 1.0

        # The case considered is (Deriaz et al 2011)'s analytic solution
        # parametrized by f0, a, R0
        self.case = 'Deriazetal'

        self.ranges = {
            'R': (0.0, pn.math.scalar.sqrt(1+2*self.a/self.R0)), # sqrt 2
            'z': (-self.R0*self.a, self.R0*self.a),
            'psi': (0.0, self.f0*self.R0*self.R0*self.a*self.a/2.0),
        }


#########################################
# Sources

# todo decorator?
def p_inside(p):
    def inside(q):
        # p is the parameters instance, and q is the test point.
        R = q[0]
        z = q[1]
        a = problem.p.a
        R0 = problem.p.R0
        # use symmetry
        z = -z if z < 0 else z
        R_bdy = R
        cosalpha_bdy = R0/(2.0*a)*((R_bdy*R_bdy)/(R0*R0)-1.0)
        # print(f"R {R}")
        # print(f"cosalpha {cosalpha_bdy}")
        alpha_bdy = pn.math.scalar.arccos(cosalpha_bdy)
        z_bdy = a*R0*pn.math.scalar.sin(alpha_bdy)
        return z <= z_bdy
    return inside

interior_0 = pn.source.Special(
    box = pn.source.Box90(
        proportions=lambda p: [p.extent('R'), p.extent('z')],
        origin=lambda p: [p.min('R'), p.min('z')],
    ),
    inside = p_inside,
    # awk
    measure = 2*1.4,
    mode = 'pseudo',
)

interior_reinforce = pn.source.Special(
    box = pn.source.Box90(
        proportions=lambda p: [p.extent('R')/3.0, p.extent('z')],
        origin=lambda p: [p.min('R'), p.min('z')],
    ),
    inside = p_inside,
    # awk
    measure = 2*1.4/3.0,
    mode = 'pseudo',
)

# You can toggle between these definitions to
# see the difference from reinforcing the point

# interior = interior_0

interior = pn.source.Union()
interior += interior_0
interior += interior_reinforce


# todo decorator?
def parametrization_p(p):
    def parametrization(alpha):
        R0 = p.R0
        a = p.a
        R = R0*pn.sqrt(1.0+2.0*a/R0*pn.cos(alpha))
        z = R0*a*pn.sin(alpha)
        return R, z
    return parametrization


bdy_interior = pn.source.Parametrized(
    parametrization=parametrization_p,
    ranges = [(0, 2*pn.pi)],
    # todo allow this, but allow None (default) and then
    #  estimate using same technique as bounding box <---- both are part of init.
    measure = 2*pn.pi, # depends on R0 in general, but that awaits PyPinnch update.
)


#########################################
# Constraints


def grad_shafranov(problem, hub):
    R, z = problem.get('R, z', hub)
    psi_RR, psi_zz, psi_R = problem.get('psi_R_R, psi_z_z, psi_R', hub)
    return pn.eq(
        LHS=R*psi_RR + R*psi_zz - psi_R,
        RHS=-R*G_exact(R, z, problem),
    )

def dirichlet_bc(problem, hub):
    psi = problem.get('psi', hub)
    return pn.eq(
        LHS=psi,
    )

constraint1 = pn.constraint.Constraint(
    label='psi_pde',
    source=interior,
    residual=grad_shafranov,
)

constraint2 = pn.constraint.Constraint(
    label='bc_bdy',
    source=bdy_interior,
    residual=dirichlet_bc,
)

constraints = [constraint1, constraint2]


#########################################


solutions = {
    "R, z; psi": pn.Solution(
        every=1,
        methods={
            'psi': 'direct',
        }
    ),
}


#########################################
# References


def psi_ref(X, problem):
    case = problem.p.case
    if case == 'Deriazetal':
        R, z = problem.get('R, z', X=X)
        return psi_exact(R, z, problem)
    else:
        raise ValueError

references = {
    "R, z; psi": pn.Reference(
        methods={
            'psi': psi_ref,
        },
    )
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


