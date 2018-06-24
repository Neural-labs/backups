import datetime
def log_(file_name, message,):
    with open(file_name, "a") as logger:
        logger.write(str(datetime.datetime.now())+": "+message+"\n")
        logger.close()

