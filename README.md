# What 

This is intended to be managed by [xrd_tool_downloader](https://github.com/OriolFilter/xrd_tool_downloader).

Will be executed by the file `BootGGXrd.bat` file located within the Xrd folder as it starts Xrd.

Note that this is not intended to be manually launched/applied.

# How

This will look for a file named `xrd_executable_list.json`.

The file should look like the following:

```json
[
  {
    "mod_name": "ibrow19/GGXrdReplayTakeover",
    "workdir": "ibrow19_GGXrdReplayTakeover",
    "dll_paths": [
      "GGXrdReplayTakeover.dll"
    ]
  },
  {
    "mod_name": "kkots/rev2-wakeup-tool",
    "workdir": "kkots_rev2-wakeup-tool",
    "executable_path": "GGXrdReversalTool.exe",
    "arguments": []
  }
]
```

# Linux?

Since it will be executed through the `BootGGXrd.bat` file, proton will handle this, meaning that only needs to work for Windows.

This also means that it can be built only from Windows.

# Notes

This tool is meant to place the .exe in the directory `GUILTY GEAR Xrd -REVELATOR-/Binaries/Win32`.

Therefore, all the paths must be relative to that location.

# Compiling

> Using virtual environments is a **good and recommended** practice, but I won't go over that.
 
> This assumes you have both, Python installed and the `pip` command.
> 
> - [How to install Python3](https://www.python.org/downloads/)
> - [How to install PIP](https://pip.pypa.io/en/stable/installation/)

## Install/Update libraries/dependencies

```shell
pip3 install -r requirements.txt
```

## Building

Locate yourself within the 

#### Linux

```shell
pyinstaller src/main.py  --clean -F --hidden-import "textual.widgets._tab_pane" --hidden-import "rich._unicode_data.unicode17-0-0"
```

#### Windows

```shell
pyinstaller src/main.py  --clean -F --hidden-import "textual.widgets._tab_pane" --hidden-import "rich._unicode_data.unicode17-0-0"  --nowindow
```


This needs to be compiled from Windows, as it is intended to run through Proton.

```shell
pyinstaller src/main.py --distpath binary_dump --name xrd_startup_launcher.exe  --clean -F --paths venv/lib/python3.14/site-packages --nowindow
```