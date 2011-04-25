import os.path

def load_track_list(path):
    with open(os.path.join("track_lists","helios.txt")) as f:
        for line in f:
            parts = line.strip().split("|")
            d = dict(artist=parts[0],album=parts[1],title=parts[2])
            yield d
