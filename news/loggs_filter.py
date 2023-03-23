import logging


def logg_filter(level):
    level = getattr(logging, level)

    def compare_logs(record):
        return record.levelno == level

    return compare_logs
