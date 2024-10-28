



import queueg as qg


mus = [
    '1.00',
    '0.50',
    '0.30',
    '0.15',
]


if __name__ == '__main__':

    for i, mu in enumerate(mus):

        run = qg.PyPinnchRun(
            location=qg.Location(
                project='pinn',
                dateYMD=qg.today(),
                runtag = f"mu{mu}",
            ),
            main_module="main",
            config_list = f"config_mu{i}",
        )

        run.start()

        post = qg.Post(run=run)
        summary = post.validation_summary("u")
        print(summary)

