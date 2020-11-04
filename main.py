import pandas as pd
import glob
from INDICATORS.RSI import RSI
from PATERNS.HD_NEGATIVE import HD_NEGATIVE
from PATERNS.HD_POSITIVE import HD_POSITIVE
from PATERNS.RD_NEGATIVE import RD_NEGATIVE
from PATERNS.RD_POSITIVE import RD_POSITIVE

CLOSE_INDEX = '<CLOSE>'
LOW_INDEX = '<LOW>'
HIGH_INDEX = '<HIGH>'
OPEN_INDEX = '<OPEN>'
VOl_INDEX = '<VOL>'
VALUE_INDEX = '<VALUE>'
NOT_INDEX = '<NOT>'
DATE_INDEX = '<DTYYYYMMDD>'

HISTORY_LENGTH = 365  # one year
if __name__ == '__main__':
    input_folder = './RAWDATA/'
    files = glob.glob(f'{input_folder}*.csv')
    for file in files:
        print(file)
        data = pd.read_csv(file)

        Opens = data[OPEN_INDEX].iloc[-HISTORY_LENGTH:]
        Highs = data[HIGH_INDEX].iloc[-HISTORY_LENGTH:]
        Lows = data[LOW_INDEX].iloc[-HISTORY_LENGTH:]
        Closes = data[CLOSE_INDEX].iloc[-HISTORY_LENGTH:]
        Volumes = data[VOl_INDEX].iloc[-HISTORY_LENGTH:]
        Values = data[VALUE_INDEX].iloc[-HISTORY_LENGTH:]

        for i in range(1, 100000):
            Closes = data[CLOSE_INDEX].iloc[-(HISTORY_LENGTH + i):-i]
            Lows = data[LOW_INDEX].iloc[-(HISTORY_LENGTH + i):-i]
            Highs = data[HIGH_INDEX].iloc[-(HISTORY_LENGTH + i):-i]
            DATE = data[DATE_INDEX].iloc[-(HISTORY_LENGTH + i):-i]

            rsi = RSI(Closes)

            HD_POSITIVE().RD(Lows, rsi, DATE)
            HD_NEGATIVE().RD(Highs, rsi, DATE)
            RD_NEGATIVE().RD(Highs, rsi, DATE)
            RD_POSITIVE().RD(Lows, rsi, DATE)


