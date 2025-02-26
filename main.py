import logging

from CommPort import CommPort, syn_read_send
from read_config import read_config


logging.basicConfig(level=logging.DEBUG)


# NOTE: the total entrance of the program
logging.info("Program started")
logging.info("Before using: ")
logging.info("""
for each port in the config file, the program will create a thread to run the port
and when which ever the port recieve, the program will send the data to the other port to send out
A port recieve -> B port send
B port recieve -> A port send
""")

logging.info("parse the config file")
configs = read_config()

logging.info("pass the arguments to the CommPort object")
comports: list[CommPort] = []
for config in configs:
    comports.append(CommPort(**config))


logging.info("add each port's write, read, or read and write syn to the threading pool")
port1 = comports[0]
port2 = comports[1]

try:
    syn_read_send(port1, port2)
except KeyboardInterrupt:
    logging.info("KeyboardInterrupt: Program terminated by user")
    logging.info("Terminated")
finally:
    port1.__close__()
    port2.__close__()
