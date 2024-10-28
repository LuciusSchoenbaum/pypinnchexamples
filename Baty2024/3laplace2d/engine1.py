

import pypinnch as pn


# test, deploy
# max_iterations1 = 2
max_iterations1 = 10
# max_iterations1 = 50
tolerance=1e-6
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


phases = {
    'P1': pn.phase.StandardPINN(
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
            pn.strategy.LRSched(
                "Exponential",
                niter=1,
            ),
        ],
        actions=[
            pn.action.Result(
                vresolution=[120],
                # skip_plots=True,
            ),
            pn.action.LossCurves(every=1),
            pn.action.monitor.BatchMonitor(),
            pn.action.monitor.SampleMonitor(
                        # show_in_view=True,
            ),
        ],
    )
}


#########################################
# Engine


engine = pn.engine.TimeIndependent(
    phases=phases,
    checkpoints=None,
    file=__file__,
)


