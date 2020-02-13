import sys
from datetime import datetime


def convert_event_to_sch_input(record):
    print(record)


def read_more_events_file(file_name):
    with open(file_name, 'r') as input_file:
        all_events = [x for x in [line.split() for line in  [x[:x.index('/')] if '/' in x else x for x in input_file]  ] if len(x)>0 and x[0][:2]!='--'] # trim comments after '/', filter out empty lines and comment lines

        events_by_object = {} 
        for item in all_events: 
            if item[0] in events_by_object.keys():
                events_by_object[item[0]].append([datetime.strptime(item[1],"%d.%m.%Y")]+item[1:])
            else:
                events_by_object.update({item[0]:[[datetime.strptime(item[1],"%d.%m.%Y")]+item[1:]]})

        for item in events_by_object:
            print()
            for x in events_by_object[item]:
                print(item, x)
            #print(item, events_by_object[item])

read_more_events_file(sys.argv[1])
