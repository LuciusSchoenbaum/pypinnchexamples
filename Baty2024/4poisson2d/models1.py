

import pypinnch as pn


if pn.cpu(pn.cuda_if_available()):
    num_dense_layers=5
    layer_size=64
else:
    num_dense_layers=6
    layer_size=512
activation="tanh"
initializer="Xavier uniform"
regularizer=None

model = pn.model.WTPNN(
    hidden_layer_sizes=[layer_size] * num_dense_layers,
    activation=activation,
    initializer=initializer,
    regularizer=regularizer,
)

models = pn.Models(
    models=model,
    file=__file__,
)


