import logging

logging.basicConfig(level=logging.DEBUG, filename="log.log", filemode="w",
                    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s - %(module)s")

logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")

#log a variable
x=10
logging.info(f"value of x is {x}")

#log a exception with stack trace
try:
    y = 1/0
except ZeroDivisionError as zde:
    logging.error("Zero Division Error Occured", exc_info=True)



