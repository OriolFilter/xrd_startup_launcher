from time import sleep
from subprocess import Popen, DEVNULL
from pathlib import Path
from dataclasses import dataclass, field
from json import loads
from datetime import datetime, timedelta
import win32gui, win32process, win32api
from abc import abstractmethod
from inject_dll import inject_multiple_dlls


class WorkdirNotFoundOrInvalid(Exception):
    """
    Raised when the workdir is not located by the Tool class, or isn't a directory.
    """
    # TODO take argument to display the name/path


class ExecutableNotFoundOrInvalid(Exception):
    """
    Raised when the executable/binary is not located, or isn't a file.
    """
    # TODO take argument to display the name/path


class DLLNotFoundOrInvalid(Exception):
    """
    Raised when the DLL to inject is not located, or isn't a file.
    """
    # TODO take argument to display the name/path


@dataclass()
class Tool:
    mod_name: str
    workdir: str
    skip: bool = False

    def __post_init__(self):
        self._post_init_checks()

    @abstractmethod
    def check_paths_exist(self):
        pass

    def _post_init_checks(self):
        self._missing_required_attributes()
        self._class_specific_checks()

    @property
    @abstractmethod
    def required_attributes(self) -> [str]:
        pass

    def _missing_required_attributes(self):
        for attribute in ["mod_name"] + self.required_attributes:
            if not getattr(self, attribute):
                raise Exception(f"{attribute} field is required")

    @abstractmethod
    def _class_specific_checks(self):
        pass

    @abstractmethod
    def launch(self):
        """
        Each one implements their own
        """
        pass


@dataclass(kw_only=True)
class BinaryExecutor(Tool):
    """
    Reserved for mods/apps/etc that require a binary to be executed (.exe)
    """
    executable_path: str
    arguments: list[str] = field(default=list)

    def _class_specific_checks(self):
        if not self.arguments:
            self.arguments = []

    @property
    def required_attributes(self) -> [str]:
        return ["executable_path"]

    def check_paths_exist(self):
        workdir = Path(self.workdir)
        if not workdir.exists() or not workdir.is_dir():
            raise WorkdirNotFoundOrInvalid
        executable = workdir.joinpath(self.executable_path)
        if not executable.exists() or not executable.is_file():
            raise DLLNotFoundOrInvalid

    def launch(self) -> bool:
        """
        Launches a process for the respective .exe file

        :param tool_object: Respective tool
        :return:
        """
        exe_full_path = ""

        process = Popen(
            shell=False,
            args=[
                Path(self.workdir).joinpath(self.executable_path),
                *self.arguments
            ],
            stdin=None,
            stdout=DEVNULL,
            stderr=DEVNULL,
            cwd=Path(self.workdir),
            start_new_session=True,
        )

        return True


@dataclass(kw_only=True)
class DLLInjector(Tool):
    """
    Reserved for mods/apps/etc that require to inject DLL files without the need of executing binary files (.exe)
    """

    dll_paths: list[str]

    def launch(self):
        # TODO error managment
        workdir = Path(self.workdir)
        dll_path_list = []
        for dll_path in self.dll_paths:
            dll_path_list.append(workdir.joinpath(dll_path))
        inject_multiple_dlls(self.dll_paths)

    @property
    def required_attributes(self) -> [str]:
        return ["dll_paths"]

    def _class_specific_checks(self):
        if not self.dll_paths:
            raise Exception("DLL files need to be specified")

    def check_paths_exist(self):
        workdir = Path(self.workdir)
        if not workdir.exists() or not workdir.is_dir():
            raise WorkdirNotFoundOrInvalid
        for dll_path in self.dll_paths:
            dll_file = workdir.joinpath(dll_path)
            if not dll_file.exists() or not dll_file.is_file():
                raise DLLNotFoundOrInvalid


def check_xrd_is_running() -> bool:
    """
    Returns true if everything OK
    :return:
    """
    window_handle = win32gui.FindWindow("LaunchUnrealUWindowsClient", "Guilty Gear Xrd -REVELATOR-")
    if window_handle == 0:
        """Xrd is not open"""
        return False
    thread_id, process_id = win32process.GetWindowThreadProcessId(window_handle)
    PROCESS_ALL_ACCESS = 0x1FFFFF
    process_handle = win32api.OpenProcess(PROCESS_ALL_ACCESS, 0, process_id)
    if not process_handle:
        """Failed to open Guilty Gear Xrd's process."""
        return False
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
        tool_info: dict
        if tool_info.get("dll_paths"):
            _tool: Tool = DLLInjector(**tool_info)
        else:
            _tool: Tool = BinaryExecutor(**tool_info)
        tools_list.append(_tool)
    del _tool

    tools_list.sort(key=lambda x: x.mod_name, reverse=False)

    print("Mods found to launch:")

    for tool_object in tools_list:
        print(f"- {tool_object.mod_name}")

    print("\nInspecting mod status:")
    for tool_object in tools_list:
        workdir = ""
        executable = ""
        print(f"\t- [{tool_object.mod_name}]:")
        try:
            tool_object.check_paths_exist()
            executable = workdir = "OK"
        except WorkdirNotFoundOrInvalid:
            workdir = "Failed. Not Found or Not a Directory"
            executable = "---"
            tool_object.skip = True
        except DLLNotFoundOrInvalid:
            workdir = "OK"
            executable = "Failed. Not Found or Not a Directory"
            tool_object.skip = True
        print(f"\t\tWorkdir: {workdir}\n\t\tExecutable: {executable}")
    del workdir, executable
    while not check_xrd_is_running():
        print("Waiting for Xrd to start")
        sleep(0.2)
    xrd_up_time = datetime.now()

    print("Xrd process found, proceeding to start the mods")

    for tool_object in tools_list:
        if tool_object.skip:
            print(f" [{tool_object.mod_name}] SKIPPED")
        else:
            tool_object: Tool
            # _last_second: int = 0
            # while (datetime.now() - xrd_up_time).seconds < timedelta(seconds=tool.delay).seconds:
            #     if _last_second != (datetime.now() - xrd_up_time).seconds:
            #         print(
            #             f" [{tool.mod_name}] waiting ({(datetime.now() - xrd_up_time).seconds}s / {tool.delay}s)")
            #         _last_second = (datetime.now() - xrd_up_time).seconds
            #
            #     sleep(0.2)
            # del _last_second
            print(f"Launching {tool_object.mod_name}")
            try:
                tool_object.launch()
                print(f" [{tool_object.mod_name}] Launched\n")
            except Exception as e:
                print(f" [{tool_object.mod_name}] Failed to launch\n\tError: {e}")

    sleep(2)
