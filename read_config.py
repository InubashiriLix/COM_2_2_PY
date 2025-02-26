from typing import Any


def read_config() -> list[dict[str, Any]]:
    try:
        with open("config.txt", "r") as file:
            file_lines = file.readlines()
            rtn_configs = []
            for line in file_lines[:2]:
                # find the COM port
                temp = line.split(" ")
                port = temp[0]
                if port[:3] != "COM":
                    raise ValueError("Invalid COM / tty port argument")
                try:
                    baudrate = int(temp[1])
                except ValueError:
                    raise ValueError("Invalid baudrate argument, should be integer")

                mode = temp[2].strip()
                if mode not in ("READONLY, WRITEONLY, READWRITE"):
                    raise ValueError(
                        "Invalid mode argument, should be READONLY, WRITEONLY, or READWRITE"
                    )
                rtn_configs.append({"port": port, "baudrate": baudrate, "mode": mode})
            return rtn_configs
    except FileNotFoundError:
        print("config file not found")
        print("please create a config.txt file with the following format:")
        print("COM1 115200 READWRITE")
        raise FileNotFoundError("config file not found")


if __name__ == "__main__":
    test_list = read_config()
