import serial
import time
import logging
import concurrent.futures

logging.basicConfig(level=logging.DEBUG)

SLEEP_TIME = 0.001  # 1ms sleep time


class CommPort:
    def __init__(self, port: str, baudrate: int, mode: str):
        self.port = port
        self.baudrate = baudrate
        self.mode = mode

        self.serial_com = serial.Serial(
            port=self.port, baudrate=self.baudrate, bytesize=8, parity="N"
        )
        if self.serial_com.is_open:
            print("Serial connection established")
        else:
            raise Exception(
                "[write port {serial.port}] Serial connection could not be established"
            )

    def send_data(self, data: bytearray) -> None:
        if self.serial_com and self.serial_com.is_open:
            self.serial_com.write(data)
        # the exception has been raised in the write function
        # if the port is not open, then raise PortNotOpenError
        # if the time out, then raise SerialTimeoutException
        # if failed then raise SerialException

    def read_data(self) -> bytearray:
        if self.serial_com and self.serial_com.is_open:
            data = bytearray(self.serial_com.readline())
            return data
        else:
            raise Exception(
                f"[read port {self.serial_com.port}] Serial connection is not open or closed"
            )

    def __close__(self) -> None:
        if self.serial_com is not None:
            self.serial_com.close()
        logging.info("Serial connection closed")


def syn_read_send(port1: CommPort, port2: CommPort) -> None:
    def forward_data(source: CommPort, desti: CommPort) -> None:
        while True:
            try:
                data = source.read_data()
                if data:
                    logging.info(
                        f"[{source.port}] Received: {data.hex()} -> Forwarding to [{desti.port}]"
                    )
                    desti.send_data(data)
                time.sleep(SLEEP_TIME)
            except Exception as e:
                logging.info(f"Error in {source.port}: {e}")
                break
        source.__close__()
        desti.__close__()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(forward_data, port1, port2)
        future2 = executor.submit(forward_data, port2, port1)
        concurrent.futures.wait([future1, future2])
