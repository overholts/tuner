from datetime import datetime


def get_temp_filename(prefix: str, extension: str):
    return "{}_{}.{}".format(prefix, int(datetime.now().timestamp()), extension)
