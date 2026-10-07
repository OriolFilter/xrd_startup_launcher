from time import sleep
import psutil
from subprocess import Popen, DEVNULL
from pathlib import Path
from dataclasses import dataclass, field
from json import loads
from datetime import datetime, timedelta


class WorkdirNotFoundOrInvalid(Exception):
    """
    Raised when the workdir is not located by the Tool class, or isn't a directory.
    """


class ExecutableNotFoundOrInvalid(Exception):
    """
    Raised when the workdir is not located by the Tool class, or isn't a file.
    """


@dataclass()
class Tool:
    mod_name: str
    workdir: str
    executable_path: str
    arguments: list[str] = field(default=list)
    delay: int = 0
    skip: bool = False

    def __post_init__(self):
        required_attributes = [
            "mod_name",
            "executable_path"
        ]
        for attribute in required_attributes:
            if not getattr(self, attribute):
                raise Exception("mod_name field is required")

        if not self.arguments:
            self.arguments = []

        if not self.delay:
            self.delay = 0

    def check_paths_exist(self):
        workdir = Path(self.workdir)
        if not workdir.exists() or not workdir.is_dir():
            raise WorkdirNotFoundOrInvalid
        executable = workdir.joinpath(self.executable_path)
        if not executable.exists() or not executable.is_file():
            raise ExecutableNotFoundOrInvalid


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
    tools_list: [Tool] = []
    json_file = Path("xrd_executable_list.json")

    if not json_file.exists() or json_file.is_file():
        print(f"File {json_file.name} either not found, or is not a regular file.")

    # Load Json
    with open(json_file, 'r', encoding="utf-8") as user_file:
        json_contents = loads(user_file.read())

    # Load tools
    for tool_info in json_contents:
        _tool: Tool = Tool(**tool_info)
        tools_list.append(_tool)
    del _tool

    tools_list.sort(key=lambda x: x.delay, reverse=False)

    print("Mods found to launch:")

    for tool in tools_list:
        print(f"- {tool.mod_name}")

    print("\nInspecting mod status:")
    for tool in tools_list:
        workdir = ""
        executable = ""
        print(f"\t- [{tool.mod_name}]:")
        try:
            tool.check_paths_exist()
            executable = workdir = "OK"
        except WorkdirNotFoundOrInvalid:
            workdir = "Failed. Not Found or Not a Directory"
            executable = "---"
            tool.skip = True
        except ExecutableNotFoundOrInvalid:
            workdir = "OK"
            executable = "Failed. Not Found or Not a Directory"
            tool.skip = True
        print(f"\t\tWorkdir: {workdir}\n\t\tExecutable: {executable}")
    del workdir, executable
    while not is_xrd_running():
        print("Waiting for Xrd to start")
        sleep(0.2)
    xrd_up_time = datetime.now()

    print("Xrd process found, proceeding to start the mods")

    for tool in tools_list:
        if tool.skip:
            print(f" [{tool.mod_name}] SKIPPED")
        else:
            tool: Tool
            _last_second: int = 0
            while (datetime.now() - xrd_up_time).seconds < timedelta(seconds=tool.delay).seconds:
                if _last_second != (datetime.now() - xrd_up_time).seconds:
                    print(
                        f" [{tool.mod_name}] waiting ({(datetime.now() - xrd_up_time).seconds}s / {tool.delay}s)")  # TODO words
                    _last_second = (datetime.now() - xrd_up_time).seconds

                sleep(0.2)
            del _last_second

            print(f"Launching {tool.mod_name}")
