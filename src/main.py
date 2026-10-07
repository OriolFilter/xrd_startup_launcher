from time import sleep
import psutil
from subprocess import Popen, DEVNULL
from pathlib import Path
from dataclasses import dataclass, field
from json import loads


@dataclass()
class Tool:
    mod_name: str
    executable_path: str
    arguments: list[str] = field(default=list)
    delay: float = 0

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

    # def load_from_json(self):
    #     pass


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

    for tool_info in json_contents:
        print(*tool_info.items())
        _tool: Tool = Tool(*tool_info.items())
        tools_list.append(_tool)

    # Json to class objects

    # Check if path exists/is valid

    # print("Mods found to launch:")
    # for file in executables:
    #     print(f"- {file}")
    #
    # while not is_xrd_running():
    #     print("Waiting for Xrd to start")
    #     sleep(0.3)
    # sleep(0)  # TODO check if it works/not, etc
    #
    # print("Xrd process found, proceeding to start the mods")
    #
    # # for file in executables:
    # #     print(f"Launching {file}")
    # #     if launch_exe(file):
    # #         print("\tStatus: Successful")
    # #     else:
    # #         print("\tStatus: Failed")
