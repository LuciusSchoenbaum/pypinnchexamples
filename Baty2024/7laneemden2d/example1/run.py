




import queueg as qg


run = qg.PyPinnchRun(
    main_module="main",
    location=qg.Location(
        locale='index',
        project='pinn',
        dateYMD=qg.today(),
    ),
)


if __name__ == '__main__':

    run.start()

    post = qg.Post(run=run)

    summary = post.validation_summary(labels='u')
    print(summary)

