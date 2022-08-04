#! /usr/bin/env python3

import asyncio
import argparse
import yaml

command_template = "./create_postfit_distributions_yaml.py --input data/{INPUTFOLDER}/{CAT}_hepdata.root --analysis-configuration analysis_configuration_grouped.yaml --output-file {CAT}_hepdata_grouped_postfit_{OUTPOSTFIX}.yaml --distribution-quantity '{QUANTITY}' --category {CAT} --output-directory submission_preparation --min-bin-content 1e-3 --signal-pattern '(.*)_(\d*)' --mode grouped {ADDITIONAL}"


async def execute_command(queue, name):
    interrupted = False
    while not queue.empty():
        task = None
        try:
            task = await queue.get()
            print(f"{name} command: {task}")
        except asyncio.CancelledError:
            print(f"{name}: shutting down due to interruption")
            interrupted = True
            return

        if task:
            try:
                sub_process = await asyncio.create_subprocess_shell(
                    task,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await sub_process.communicate()
                print(f"{name}: returncode for {task}: {sub_process.returncode}")
                if sub_process.returncode != 0:
                    print(f"{name}: error for {task}:\n{stderr.decode('utf-8')}")
            except asyncio.CancelledError:
                interrupted = True
                print(f"{name}: cancelling subprocess due to interruption")
                sub_process.terminate()
                return
            queue.task_done()
        else:
            continue
    return


async def main(n_threads, commands):
    creation_task_queue = asyncio.Queue()

    create_worker = []
    for i in range(n_threads):
        task = asyncio.ensure_future(
            execute_command(creation_task_queue, f"create_worker_{i}")
        )
        create_worker.append(task)

    for command in commands:
        await creation_task_queue.put(command)

    try:
        await creation_task_queue.join()
    except asyncio.CancelledError:
        print("main: Caught Interruption...")
    finally:
        for index, task in enumerate(create_worker):
            print(f"Cancelling task {index}")
            task.cancel()
        await asyncio.gather(*create_worker, return_exceptions=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script to create postfit shapes for HEPData queue-based"
    )
    parser.add_argument(
        "--n-threads", required=True, type=int, help="Number of threads to be used"
    )
    parser.add_argument(
        "--categories-configurations",
        required=True,
        nargs="+",
        help="Individual configuration of shapes for groups of categories",
    )

    args = parser.parse_args()
    commands = []
    for confname in args.categories_configurations:
        conf = yaml.load(open(confname, "r"), Loader=yaml.FullLoader)
        for c in conf["catlist"]:
            additional = ""
            if conf["additional_inputs"] and conf["additional_signals"]:
                additional = " ".join(
                    [
                        "--additional-inputs",
                        conf["additional_inputs"].format(CAT=c),
                        "--additional-signals",
                        "'" + conf["additional_signals"] + "'",
                    ]
                )
            command = command_template.format(
                CAT=c,
                QUANTITY=conf["quantity"],
                INPUTFOLDER=conf["input_folder"],
                OUTPOSTFIX=conf["output_file_postfix"],
                ADDITIONAL=additional,
            ).strip()
            commands.append(command)

    try:
        asyncio.run(main(args.n_threads, commands))
    except asyncio.CancelledError:
        pass
