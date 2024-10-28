

import pypinnch as pn


# test, deploy
max_iterations1 = 10
tolerance=1e-5
learning_rate = 1e-3
gamma = 0.8
weights = {}
if pn.cpu(pn.cuda_if_available()):
    batchsize=16
    SPL=16
    # batchsize=128
    # SPL=128
else:
    batchsize=512
    SPL=128


phase1 = pn.phase.StandardPINN(
    handle="P1",
    weights=weights,
    batchsize=batchsize,
    SPL=SPL,
    strategies=[
        pn.strategy.Optimizer(
            label="LBFGS",
            kit=pn.Kit(
                tolerance=tolerance,
                max_iterations=max_iterations1,
                learning_rate=learning_rate,
                gamma=gamma,
            )
        ),
        pn.strategy.LRSched("Exponential"),
    ],
    actions=[
        pn.action.Result(
            vresolution=[120],
            # skip_plots=True,
        ),
        pn.action.LossCurves(every=1),
        # pn.action.monitor.BatchMonitor(), # todo error on timeindependent
        pn.action.monitor.SampleMonitor(
                    # show_in_view=True,
        ),
    ],
)




phases = [phase1]



#########################################
# Drivers


driver = pn.Driver(
    phases=phases,
    config=pn.DriverConfig(
        handle="D1",
    ),
    strategies=[],
    actions=[],
)

drivers = [driver]


#########################################
# Engine


engine = pn.engine.TimeIndependent(
    handle="E1",
    drivers=drivers,
    checkpoints=None,
    file=__file__,
)


