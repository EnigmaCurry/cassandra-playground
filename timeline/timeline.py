# A timeline of events.
#  * Record events for certain timestamps
#  * Retrieve events for a given date range

# This example should be tolerant of multiple clients writing events
# at a time. For this to work reliably, we should use version 1 UUIDs
# as column keys so that two clients wishing to record data at the
# exact same time do not fight for the same key. This has the drawback
# that we cannot use the column key as the time of the event, so we
# need to encode that into the column value itself. This could also be
# done with SuperColumn families to split the timestamp from the
# message itself, but with simplistic data like this, it's probably
# overkill.

# Schema:
# timeline = {
#   '2011-05-01' : {
#      UUID('xxx'): "timestamp|event_message",
#      UUID('yyy'): "timestamp|event_message"
#   },
#   '2011-05-02' : {
#      UUID('zzz'): "timestamp|event_message"
#   },
# }

# Keyspace created in pycassaShell:
#
#  SYSTEM_MANAGER.create_keyspace('Timeline', replication_factor=1)
#  SYSTEM_MANAGER.create_column_family('Timeline', 'timeline',
#      comparator_type=pycassa.system_manager.TIME_UUID_TYPE)

import pycassa
from time import mktime
import random
from datetime import datetime, timedelta
import unittest

class Timeline(object):
    def __init__(self, column_family):
        self.column_family = column_family
    def append(self, event, time=None):
        """Add an event with the given time.
        If time is None, the time is the current time."""
        if time is None:
            time = datetime.now()
        #Since we're using UUIDs for column names, we can't get the
        #time of the event back, so let's encode the time into the
        #value itself with the format: "timestamp|event_message".
        self.column_family.insert(self.__datetime_to_cf_key(time),
                                  {time:self.__encode_event(event,time)})
    def get_events_between(self, start, finish):
        "Return all the events in the given date range"
        events = []
        #Range should be non-inclusive of finish, so subtract one millisecond:
        finish = finish - timedelta(milliseconds=1)
        #Iterate over each day from start to finish:
        #Start with start stripped of it's hours, minutes, seconds:
        date = datetime(*start.timetuple()[:3])
        while date <= finish:
            #Query events for each day in between start and finish:
            events.extend(self.__get_days_events(date, start, finish))
            #Increment to the next day:
            date = date + timedelta(1)
        return events
    def __get_days_events(self, date, start, finish):
        try:
            for event in self.column_family.get(
                self.__datetime_to_cf_key(date),
                column_start=start, column_finish=finish).values() :
                yield self.__decode_event(event)
        except pycassa.NotFoundException:
            return
    def __encode_event(self, event, date):
        return "%s|%s" % (mktime(date.timetuple()), event)
    def __decode_event(self, value):
        timestamp, event = value.split("|",1)
        date = datetime.fromtimestamp(float(timestamp))
        return (date, event)
    def __datetime_to_cf_key(self, date):
        "Create a column family key from a datetime"
        return date.strftime("%Y-%m-%d")

class TimelineTest(unittest.TestCase):
    def setUp(self):
        self.pool = pycassa.connect("Timeline")
        self.cf = pycassa.ColumnFamily(self.pool, "timeline")
        self.cf.truncate()

    def generate_events(self, n=100, start=None, finish=None):
        "Generate n events on random dates between start and finish."
        if start is None:
            start = datetime(2011,1,1)
        if finish is None:
            finish = datetime(2012,1,1)
        start = mktime(start.timetuple())
        finish = mktime(finish.timetuple())
        for i in xrange(n):
            d = datetime.fromtimestamp(random.randint(start,finish))
            yield (d,"Event {0}".format(i+1))

    def writeRandomEvents(self, timeline, preseed_events=None):
        #Generate 100 random events for May 2011.
        #Keep the event list around so we can verify them later:
        events = list(self.generate_events(100,start=datetime(2011,5,1),
                                           finish=datetime(2011,6,1)))
        if preseed_events:
            events.extend(preseed_events)
        #Add these events to the timeline:
        for date, msg in events:
            timeline.append(msg, time=date)
        #Also add some events for the rest of the year to add noise:
        for date, msg in self.generate_events(400, start=datetime(2011,1,1),
                                         finish=datetime(2011,5,1)):
            timeline.append(msg, time=date)
        for date, msg in self.generate_events(400, start=datetime(2011,6,1),
                                         finish=datetime(2012,1,1)):
            timeline.append(msg, time=date)
        return events
    
    def testEventOrder(self):
        "Test writing and retrieving of events in chronological order"
        timeline = Timeline(self.cf)
        events = self.writeRandomEvents(timeline)
        #Now get all the events for May back in order:
        may_events = timeline.get_events_between(datetime(2011,5,1),
                                                 datetime(2011,6,1))
        #Ensure that the events are the same, and that they are in chron order:
        self.assertEqual(may_events,sorted(events))

    def testDateExtremeties(self):
        """Make sure events just inside/outside the date range are
        (or are not) included."""
        timeline = Timeline(self.cf)
        #Add a few hand crafted events for date extremities:
        first_event = (datetime(2011,5,1), "Very First Event of May")
        last_event = (datetime(2011,6,1)-timedelta(seconds=1),
                       "Very Last Event of May")
        march_event = (datetime(2011,5,1)-timedelta(seconds=1),
                       "Very Last Event of March")
        june_event = (datetime(2011,6,1), "Very First Event of June")
        events = [first_event,last_event]
        events = self.writeRandomEvents(timeline, events)
        #Now get all the events for May back in order:
        may_events = timeline.get_events_between(datetime(2011,5,1),
                                                 datetime(2011,6,1))
        self.assertEqual(may_events[0], first_event)
        self.assertEqual(may_events[-1], last_event)
        self.assertTrue(march_event not in may_events)
        self.assertTrue(june_event not in may_events)
        
    def testMultiClients(self):
        "Simulate multiple clients by writing the same events twice"
        timeline = Timeline(self.cf)        
        events = list(self.generate_events(100,start=datetime(2011,5,1),
                                           finish=datetime(2011,6,1)))
        #Write the event once:
        for date, event in events:
            timeline.append(event, time=date)
        #Write the event twice:
        for date, event in events:
            timeline.append(event, time=date)
        #Now each event should be in the db twice, simulating two
        #clients writing the same events at the same time:
        may_events = timeline.get_events_between(datetime(2011,5,1),
                                                 datetime(2011,6,1))
        self.assertEqual(len(may_events), 200)
        
    def testTightDateRange(self):
        "Can we get events for just a single hour of the day?"
        timeline = Timeline(self.cf)        
        hour_events = [
            (datetime(2011,5,11,12,01),"Mid-day event 1"),
            (datetime(2011,5,11,12,05),"Mid-day event 2"),
            (datetime(2011,5,11,12,33),"Mid-day event 3"),
            ]
        other_events = [
            (datetime(2011,5,11,8,01),"Other event 1"),
            (datetime(2011,5,11,9,01),"Other event 2"),
            (datetime(2011,5,11,15,01),"Other  event 3"),
            ]
        for date, event in hour_events:
            timeline.append(event, time=date)
        for date, event in other_events:
            timeline.append(event, time=date)
        #Get all the events:
        all_events = timeline.get_events_between(datetime(2011,5,11),
                                                 datetime(2011,5,12))
        self.assertEqual(len(all_events), 6)
        #Get just the events for the hour:
        db_hour_events = timeline.get_events_between(datetime(2011,5,11,12,00),
                                                 datetime(2011,5,11,13,00))
        self.assertEqual(db_hour_events, hour_events)
