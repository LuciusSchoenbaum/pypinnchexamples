




import queueg as qg


run = qg.PyPinnchRun(
    location=qg.Location(
        project='pinn',
        dateYMD=qg.today(),
    ),
    main_module="main",
)


if __name__ == '__main__':

    run.start()

    post = qg.Post(run=run)

    summary = post.validation_summary(label='u, mu')
    print(summary)


