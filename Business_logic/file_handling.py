import pandas as pd
from pymavlink import mavutil


class FileHandling:

    def __init__(self, path: str):
        self.path = path

    def run(self) -> pd.DataFrame:
        df_points = self._extarct_coords_from_bin_file()
        df_points = self._drop_duplicait(df_points)
        df_points = self._removing_nearby_points(df_points, 40)
        return df_points

    def _extarct_coords_from_bin_file(self) -> pd.DataFrame:
        mav = mavutil.mavlink_connection(self.path)
        betch = []
        dfs = []
        while True:
            msg = mav.recv_match(type="GPS", blocking=False)
            if msg is None:
                break
            if hasattr(msg, "I") and msg.I == 1:
                betch.append((msg.Lat, msg.Lng))
            if len(betch) >= 10_000:
                dfs.append(pd.DataFrame(betch, columns=["Lat", "Lng"]))
                betch.clear()
        if betch:
            dfs.append(pd.DataFrame(betch, columns=["Lat", "Lng"]))

        df = pd.concat(dfs, ignore_index=True)
        return df

    def _drop_duplicait(self, df_points: pd.DataFrame) -> pd.DataFrame:
        shifted = df_points.shift()
        comparison = df_points == shifted
        same_as_prev = comparison.all(axis=1)
        filterd = df_points.loc[~same_as_prev]
        filterd.reset_index(drop=True)
        return filterd

    def _removing_nearby_points(self, df_points: pd.DataFrame, n: int) -> pd.DataFrame:
        df_reduced = df_points.iloc[::n].reset_index(drop=True)
        return df_reduced
