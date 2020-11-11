import pandas as pd
import glob
import numpy as np

from INDICATORS.MACD import macd
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
DATE_J_INDEX = '<DTYYYYMMDD>'

HISTORY_LENGTH = 480  # one year
divergences = []

if __name__ == '__main__':
    input_folder = './RAWDATA/'
    output_folder = './OUTPUT/'

    files = glob.glob(f'{input_folder}*.csv')
    for file in files:
        try:
            # region read data and set variables
            data = pd.read_csv(file)
            if len(data) != 0:

                TICKER = data[TICKER_INDEX].to_numpy()[-1]
                Opens = data[OPEN_INDEX].iloc[-HISTORY_LENGTH:]
                Highs = data[HIGH_INDEX].iloc[-HISTORY_LENGTH:]
                Lows = data[LOW_INDEX].iloc[-HISTORY_LENGTH:]
                Closes = data[CLOSE_INDEX].iloc[-HISTORY_LENGTH:]
                Volumes = data[VOl_INDEX].iloc[-HISTORY_LENGTH:]
                Values = data[VALUE_INDEX].iloc[-HISTORY_LENGTH:]
                DATE_J = data[DATE_J_INDEX].iloc[-HISTORY_LENGTH:]
                # endregion
                now_DATE_J = DATE_J.to_numpy()[-1]
                Volumes = Volumes.to_numpy()

                # region VDV
                VDV10 = 0
                VDV30 = 0
                VDV60 = 0
                VDV100 = 0
                length = len(Volumes)
                if len(Volumes) >= 11:
                    average_volume_10 = np.average(Volumes[length - 11:-1])
                    VDV10 = round(Volumes[-1] / average_volume_10, 2)
                if len(Volumes) >= 31:
                    average_volume_30 = np.average(Volumes[length - 31:-1])
                    VDV30 = round(Volumes[-1] / average_volume_30, 2)

                if len(Volumes) >= 61:
                    average_volume_60 = np.average(Volumes[length - 61:-1])
                    VDV60 = round(Volumes[-1] / average_volume_60, 2)

                if len(Volumes) >= 101:
                    average_volume_100 = np.average(Volumes[length - 101:-1])
                    VDV100 = round(Volumes[-1] / average_volume_100, 2)

                # endregion

                _rsi14 = RSI(Closes, 14)
                _macd = macd(Closes)
                _macd_diff = _macd._macd_diff


                # region RD 14
                out = HD_POSITIVE().RD(Lows, _rsi14, DATE_J)
                if len(out) != 0:
                    for lines in out:
                        divergences.append([now_DATE_J, TICKER, 'HD+', 'RSI14', VDV10, VDV30, VDV60, VDV100, lines])

                out = HD_NEGATIVE().RD(Highs, _rsi14, DATE_J)
                if len(out) != 0:
                    for lines in out:
                        divergences.append([now_DATE_J, TICKER, 'HD-', 'RSI14', VDV10, VDV30, VDV60, VDV100, lines])
                out = RD_NEGATIVE().RD(Highs, _rsi14, DATE_J)
                if len(out) != 0:
                    for lines in out:
                        divergences.append([now_DATE_J, TICKER, 'RD-', 'RSI14', VDV10, VDV30, VDV60, VDV100, lines])
                out = RD_POSITIVE().RD(Lows, _rsi14, DATE_J)
                if len(out) != 0:
                    for lines in out:
                        divergences.append([now_DATE_J, TICKER, 'RD+', 'RSI14', VDV10, VDV30, VDV60, VDV100, lines])
                # endregion


                # # region MACD
                # out = HD_POSITIVE().RD(Lows, _macd_diff, DATE_J)
                # if len(out) != 0:
                #     for lines in out:
                #         divergences.append(
                #             [now_DATE_J, TICKER, 'HD+', 'MACD', VDV10, VDV30, VDV60, VDV100, lines])
                # out = HD_NEGATIVE().RD(Highs, _macd_diff, DATE_J)
                # if len(out) != 0:
                #     for lines in out:
                #         divergences.append(
                #             [now_DATE_J, TICKER, 'HD-', 'MACD', VDV10, VDV30, VDV60, VDV100, lines])
                # out = RD_NEGATIVE().RD(Highs, _macd_diff, DATE_J)
                # if len(out) != 0:
                #     for lines in out:
                #         divergences.append(
                #             [now_DATE_J, TICKER, 'RD-', 'MACD', VDV10, VDV30, VDV60, VDV100, lines])
                # out = RD_POSITIVE().RD(Lows, _macd_diff, DATE_J)
                # if len(out) != 0:
                #     for lines in out:
                #         divergences.append(
                #             [now_DATE_J, TICKER, 'RD+', 'MACD', VDV10, VDV30, VDV60, VDV100, lines])
                # # endregion

        except:
            print(file)

    pd.DataFrame(divergences).to_csv('OUTPUT/divergence.csv', index=False, encoding="utf-8-sig",
                                     header=['تاریخ', "نماد", "پترن", "ایندیکاتور", "حجم نسبت به 10 روز",
                                             "حجم نسبت به 30 روز", "حجم نسبت به 60 روز", "حجم نسبت به 100 روز",
                                             "خط پترن", ]
                                     )
