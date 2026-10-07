def is_xrd_running() -> bool:
    return False


def launch_exe(path: str) -> bool:
    return False


if __name__ == '__main__':
    executables = ["1", "2", "3"]

    # Check if path exists/is valid

    print("Mods found to launch:")
    for file in executables:
        print(f"- {file}")

    while not is_xrd_running():
        print("Waiting for Xrd to start")
        pass
    print("Xrd process found, proceeding to start the mods")

    for file in executables:
        print(f"Launching {file}")
        if launch_exe(file):
            print("\tStatus: Successful")
        else:
            print("\tStatus: Failed")
