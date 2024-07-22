import logging
import sys

# https://stackoverflow.com/questions/14058453/making-python-loggers-output-all-messages-to-stdout-in-addition-to-log-file
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s - %(module)s")

logger = logging.getLogger(__name__)

#
console_output_handler = logging.StreamHandler(sys.stdout)
console_output_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s - %(module)s")
console_output_handler.setFormatter(formatter)

logger.addHandler(console_output_handler)

logger.info("Test the custom logger")

def add(a,b):
    c = a+b
    logger.info(f"{a} + {b} = {c}")

add(1,2)

