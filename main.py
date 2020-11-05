import pandas as pd
import glob
from INDICATORS.RSI import RSI
from PATERNS.HD_NEGATIVE import HD_NEGATIVE
from PATERNS.HD_POSITIVE import HD_POSITIVE
from PATERNS.RD_NEGATIVE import RD_NEGATIVE
from PATERNS.RD_POSITIVE import RD_POSITIVE

TICKER_INDEX = '<TICKER>'
CLOSE_INDEX = '<CLOSE>'
LOW_INDEX = '<LOW>'
HIGH_INDEX = '<HIGH>'
OPEN_INDEX = '<OPEN>'
VOl_INDEX = '<VOL>'
VALUE_INDEX = '<VALUE>'
NOT_INDEX = '<NOT>'
DATE_INDEX = '<DTYYYYMMDD>'

HISTORY_LENGTH = 730  # one year
HD_POS = []
HD_NEG = []
RD_POS = []
RD_NEG = []

if __name__ == '__main__':
    input_folder = './RAWDATA/'
    files = glob.glob(f'{input_folder}*.csv')
    for file in files:
        try:
            print(file)
            data = pd.read_csv(file)

            TICKER = data[TICKER_INDEX].iloc[-HISTORY_LENGTH:]
            Opens = data[OPEN_INDEX].iloc[-HISTORY_LENGTH:]
            Highs = data[HIGH_INDEX].iloc[-HISTORY_LENGTH:]
            Lows = data[LOW_INDEX].iloc[-HISTORY_LENGTH:]
            Closes = data[CLOSE_INDEX].iloc[-HISTORY_LENGTH:]
            Volumes = data[VOl_INDEX].iloc[-HISTORY_LENGTH:]
            Values = data[VALUE_INDEX].iloc[-HISTORY_LENGTH:]
            DATE = data[DATE_INDEX].iloc[-HISTORY_LENGTH:]

            rsi = RSI(Closes)

            name = TICKER.to_numpy()[-1]
            out = HD_POSITIVE().RD(Lows, rsi, DATE)
            if len(out) != 0:
                HD_POS.append([name, out])
            out = HD_NEGATIVE().RD(Highs, rsi, DATE)
            if len(out) != 0:
                HD_NEG.append([name, out])
            out = RD_NEGATIVE().RD(Highs, rsi, DATE)
            if len(out) != 0:
                RD_NEG.append([name, out])
            out = RD_POSITIVE().RD(Lows, rsi, DATE)
            if len(out) != 0:
                RD_POS.append([name, out])
        except:
            print('except')
    pd.DataFrame(HD_POS).to_csv('OUTPUT/HD_POS.csv')
    pd.DataFrame(HD_NEG).to_csv('OUTPUT/HD_NEG.csv')
    pd.DataFrame(RD_POS).to_csv('OUTPUT/RD_POS.csv')
    pd.DataFrame(RD_NEG).to_csv('OUTPUT/RD_NEG.csv')
