




import queueg as qg



if __name__ == '__main__':

    run = qg.PyPinnchRun(
        location=qg.Location(
            project='pinn',
            dateYMD = qg.today(),
        ),
        main_module="main",
    )

    run.start()

    post = qg.Post(run=run)

    summary = post.validation_summary('psi')
    print(summary)

