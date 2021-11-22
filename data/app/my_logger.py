import logging
import os
from logging.handlers import RotatingFileHandler

def initLogger(logger, logName='logs/mylog.log', _formater = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    logger.setLevel(logging.DEBUG)
    # create a file handler
    handler = RotatingFileHandler(logName, maxBytes=10000, backupCount=10)
    handler.setLevel(logging.DEBUG)
    # create a logging format
    if _formater:
        print("Using formater")
        formatter = logging.Formatter(_formater)
        handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger

def initTimeAnalysis_logger():
    # while filename exists 
    num = 0
    logName = "logs/timeTrials/{}.json".format(num)
    # if a log file exists and its not empty then create a new one
    while os.path.isfile(logName) and os.stat(logName).st_size != 0:
        num += 1
        logName = "logs/timeTrials/{}.json".format(num)
    timeLog = logging.getLogger('timeLogger')
    initLogger(timeLog, logName=logName, _formater=None)
    return timeLog