import logging
import os
from logging.handlers import RotatingFileHandler

# I don't need global loggers because if you getLogger of the same name it will return the same logger
class my_logger():
    def __new__(self, name:str, _fileName:str = 'logs/mylog.log', _formater = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        if len(_fileName) > 0:
            handler = RotatingFileHandler(_fileName, maxBytes=10000, backupCount=10)
            handler.setLevel(logging.DEBUG)
        else:
            # Should be a handler to the console 
            pass
        if _formater:
            formatter = logging.Formatter(_formater)
            handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return self.logger


# Inits the Event Logger and returns it
def initEvent_Logger():
    eventLog = my_logger('eventLogger')
    return eventLog


def initTimeAnalysis_logger(folderName:str = 'timeTrials'):
    num = 0
    logFileName = f"logs/{folderName}/{num}.json"
    # if a log file exists and its not empty then create a new one
    # I think I could use enumerate here but I'm not sure
    while os.path.isfile(logFileName) and os.stat(logFileName).st_size != 0:
        num += 1
        logFileName = f"logs/{folderName}/{num}.json"
    timeLog = my_logger(name='timeLogger', _fileName=logFileName, _formater=None)
    return timeLog