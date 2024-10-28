




import queueg as qg


sourceterm_cases = [
    '1',
    # 'a',
    # 'b',
    # 'c',
    # 'd',
    # 'e',
]
bc_cases = [
    'dir',
    # 'neu',
    # 'mix',
]




if __name__ == '__main__':

    # > assemble the combined list the loop will use
    runtags = []
    config_lists = {}
    print_strings = {}
    for c in sourceterm_cases:
        for bcc in bc_cases:
            runtag = f"{c}_{bcc}"
            runtags.append(f"{c}_{bcc}")
            config_lists[runtag] = f"config_{c}, config_bc_{bcc}"
            bcstr = "Dirichlet" if bcc == 'dir' else "Neumann" if bcc == 'neu' else "mixed"
            print_strings[runtag] = c + "\t" + bcstr + "\t"
    # > runs
    for runtag in runtags:

        run = qg.PyPinnchRun(
            location=qg.Location(
                project='pinn',
                dateYMD=qg.today(),
                runtag = runtag,
            ),
            main_module="main",
            config_list = config_lists[runtag],
        )

        run.start()

        post = qg.Post(run = run)
        val = post.validation(labels='u')
        print_strings[runtag] = print_strings[runtag] + f"{val.value:.2}"
        summary = post.validation_summary(labels='u')
        print(summary)
        # todo: did it tolout, or did it maxout?


    for runtag in runtags:
        print(print_strings[runtag])


