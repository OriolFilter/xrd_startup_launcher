from time import sleep
import psutil
from subprocess import Popen, DEVNULL
from pathlib import Path


def is_xrd_running() -> bool:
    for pid in psutil.process_iter():
        if pid.name() == "GuiltyGearXrd.exe":
            return True


def launch_exe(cwd: Path, executable: Path, args: [str]) -> bool:
    """
    Launches a process for the respective .exe file

    :param cwd: Workdir from which launch the .exe file. Assumes that always will be the parent dir from the .exe file.
    :param executable: Filename to execute
    :param args: Arguments to add/use
    :return:
    """
    exe_full_path = ""

    process = Popen(
        shell=False,
        args=[
            cwd.joinpath(executable).absolute(),
            *args,
        ],
        stdin=None,
        stdout=DEVNULL,
        stderr=DEVNULL,
        cwd=cwd,
        start_new_session=True,
    )

    return True


if __name__ == '__main__':
    delay_seconds = 0
    executables = ["1", "2", "3"]

    # Check if path exists/is valid

    print("Mods found to launch:")
    for file in executables:
        print(f"- {file}")

    while not is_xrd_running():
        print("Waiting for Xrd to start")
        sleep(0.3)
    sleep(delay_seconds)  # TODO check if it works/not, etc

    print("Xrd process found, proceeding to start the mods")

    for file in executables:
        print(f"Launching {file}")
        if launch_exe(file):
            print("\tStatus: Successful")
        else:
            print("\tStatus: Failed")
