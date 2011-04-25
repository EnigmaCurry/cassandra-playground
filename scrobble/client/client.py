#Just a test client... not actually useful:

import os.path
import json

import os.path
import urllib2
import urlparse

import cookielib
cj = cookielib.LWPCookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

host = "http://localhost:6543"

def post_json(path, data=None):
    url = urlparse.urljoin(host,path)
    data = json.dumps(data)
    u = urllib2.urlopen(url, data)
    d = u.read()
    j = json.loads(d)
    return j

def load_track_list(path):
    with open(path) as f:
        for line in f:
            parts = line.strip().split("|")
            d = dict(artist=parts[0],album=parts[1],title=parts[2])
            yield d

def test():
    user = post_json("/api/login",{"username":"ryan","password":"asdf"})
    for track in load_track_list(os.path.join("track_lists","helios.txt")):
        print("sending: {0}".format(track))
        post_json("/api/track_listen", track)
        
if __name__ == "__main__":
    test()
