from pymavlink import mavutil
from geopy.distance import geodesic


class FileHandling():

    def __init__(self, path):
        self.path = path

    def run(self):
        points = self.extarct_coords_from_bin_file()
        # print(len(points))
        updateted_points = self.removing_nearby_points(points)
        # print(len(updateted_points))
        return updateted_points
    
    def extarct_coords_from_bin_file(self):
        mav = mavutil.mavlink_connection(self.path)
        points = []
        while True:
            msg = mav.recv_match(type='GPS', blocking=False)  
            if msg is None:
                break
            if hasattr(msg, "I") and msg.I == 1:
                points.append((msg.Lat, msg.Lng))
        return points

    def removing_nearby_points(self, points):
        return points[::40]
      

