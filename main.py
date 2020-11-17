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

HISTORY_LENGTH = 260  # one year
divergences = []
Volume = []

if __name__ == '__main__':
    input_folder = './RAWDATA/'
    output_folder = './OUTPUT/'

    files = glob.glob(f'{input_folder}*.csv')
    for file in files:

        data = pd.read_csv(file)
        if len(data) != 0:
            TICKER = data[TICKER_INDEX].to_numpy()[-1]

            HL = HISTORY_LENGTH if len(data) > HISTORY_LENGTH else len(data)

            DATE_J = data[DATE_J_INDEX].iloc[-HL:]
            now_DATE_J = DATE_J.to_numpy()[-1]
            if now_DATE_J == 13990827:

                Opens = data[OPEN_INDEX].iloc[-HL:]
                Highs = data[HIGH_INDEX].iloc[-HL:]
                Lows = data[LOW_INDEX].iloc[-HL:]
                Closes = data[CLOSE_INDEX].iloc[-HL:]
                Volumes = data[VOl_INDEX].iloc[-HL:]
                Values = data[VALUE_INDEX].iloc[-HL:]
                Volumes = Volumes.to_numpy()
                Highs_np = Highs.to_numpy()
                Lows_np = Lows.to_numpy()

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
                # region DT
                DT30 = 0
                DT60 = 0
                DT100 = 0

                max_high = np.max(Highs_np[:-1])
                DT = round(1 - (Lows_np[-1] / max_high), 2) * 100


                # endregion
                Volume.append([now_DATE_J, TICKER, VDV10, VDV30, VDV60, VDV100, f'{DT}%'])

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

                # region MACD
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
                # endregion

    if len(divergences) != 0:
        pd.DataFrame(divergences).to_csv('OUTPUT/divergence.csv', index=False, encoding="utf-8-sig",
                                         header=['تاریخ', "نماد", "پترن", "ایندیکاتور", "حجم نسبت به 10 روز",
                                                 "حجم نسبت به 30 روز", "حجم نسبت به 60 روز", "حجم نسبت به 100 روز",
                                                 "خط پترن", ]
                                         )
    if len(Volume) != 0:
        Volume.sort(key=lambda x: x[3], reverse=True)
        pd.DataFrame(Volume).to_csv('OUTPUT/VDV.csv', index=False, encoding="utf-8-sig",
                                    header=['تاریخ', "نماد", "حجم نسبت به 10 روز",
                                            "حجم نسبت به 30 روز", "حجم نسبت به 60 روز", "حجم نسبت به 100 روز",
                                            "فاصله از سقف",
                                            ]
                                    )
