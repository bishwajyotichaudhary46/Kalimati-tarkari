from kalimati_tarkari.logger import logging
from kalimati_tarkari.exception import KalimatiException
import sys

logging.info('Welcome to our log')


try:
    a = 2/0
except Exception as e:
    raise KalimatiException(e, sys)
