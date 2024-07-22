import logging

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s - %(module)s")

logger = logging.getLogger(__name__)

#
handler = logging.FileHandler('test.log')
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s - %(module)s")
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info("Test the custom logger")

def add(a,b):
    c = a+b
    logger.info(f"{a} + {b} = {c}")

add(1,2)