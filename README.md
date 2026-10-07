# What 

This is intended to be managed by [xrd_tool_downloader](https://github.com/OriolFilter/xrd_tool_downloader).

Will be executed by the file `BootGGXrd.bat` file located within the Xrd folder as it starts Xrd.

# How

This will look for a file named `xrd_executable_list.json`.

The file should look like the following:

```json
[
  {
    "mod_name": "abcd_1234",
    "arguments": ["1","2","-XYZ"],
    "workdir": "path/to/workdir/folder",
    "executable_path": "path/relative/to/workdir",
    "delay": 0
  },
  {}
]
```

[//]: # (    How many seconds wait since Xrd was detected to be started
[//]: # (    "cwd": "./desired_workdir", # this could be removed)

# Linux?

Since it will be executed through the `BootGGXrd.bat` file, proton will handle this, meaning that only needs to work for Windows.

#

This tool is meant to place the .exe in the directory `GUILTY GEAR Xrd -REVELATOR-/Binaries/Win32`.

Therefore, all the paths must be relative to that location.

## Compiling

This needs to be compiled from Windows, as it is intended to run through Proton.

```shell
pyinstaller src/main.py --distpath binary_dump --name xrd_startup_launcher.exe  --clean -F --paths venv/lib/python3.14/site-packages --nowindow
```