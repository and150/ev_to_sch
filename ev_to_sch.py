import sys
from datetime import datetime


'''
def convert_event_to_sch_input(record):
    print(record)


def perf_print(object_name, event_key, event):
    perforation_multiplier = float(event[4])
    if perforation_multiplier > 0: 
        print(f"{event_key[0]:%d.%m.%Y}\t{object_name}\t\tPERFORATION\t\t{event[0]}\t{event[1]}\t{float(event[2])*2:.4f}\t{event[3]}")
        if perforation_multiplier != 1:
            print(f"{event_key[0]:%d.%m.%Y}\t{object_name}\t\tCF-MULTIPLIER\t{event[2]}\t{event[3]}\t{float(event[4])}")
    else:
        print(f"{event_key[0]:%d.%m.%Y}\t{object_name}\t\tSQUEEZE\t\t\t{event[0]}\t{event[1]}\t{float(event[2])*2:.4f}\t{event[3]}")

def wlta_print(object_name, event):
    print(f"WELLNAME\t{object_name}\n\t{event[0]:%d.%m.%Y}\tKEYWORD WVFPDP\n\t{event[2]}")

def wugr_print(object_name, event):
    print(f"WELLNAME\t{object_name}\n\t{event[0]:%d.%m.%Y}\tKEYWORD WGRUPCON\n\tYES\t{event[2]}\tLIQ")

def plim_print(object_name, event): # !!!! not realy reads PLIM event (hardcoded only the WCT limit) !!!!
    print(f"WELLNAME\t{object_name}\n\t{event[0]:%d.%m.%Y}\tKEYWORD WECON\n\t2*\t{event[3]}\t2* WELL") # no redd

def prod_print(object_name, event):
    pass
    '''

'''
############### try 2 #############
def unload_perf(object_events):
    for x in [f for f in object_events if f[2]=='PERF']:
        perforation_multiplier = float(x[3][4])
        if perforation_multiplier > 0: 
            print(f"{x[1]:%d.%m.%Y}\t{x[0]}\t\tPERFORATION\t\t{x[3][0]}\t{x[3][1]}\t{float(x[3][2])*2:.4f}\t{x[3][3]}")
            if perforation_multiplier != 1:
                print(f"{x[1]:%d.%m.%Y}\t{x[0]}\t\tCF-MULTIPLIER\t{x[3][0]}\t{x[3][1]}\t{float(x[3][4])}")
        else:
            print(f"{x[1]:%d.%m.%Y}\t{x[0]}\t\tSQUEEZE\t\t\t{x[3][0]}\t{x[3][1]}\t{float(x[3][2])*2:.4f}\t{x[3][3]}")

def unload_gconprod(object_events):

    gopt = [x for x in object_events if x[2]=='GOPT']
    gpli = [x for x in object_events if x[2]=='GPLI']
    combo = {}

    for x in gopt:
        if x[1] in combo:
            combo[x[1]].append(x)
        else:
            combo.update({x[1]:x})

    for x in gpli:
        if x[1] in combo:
            combo[x[1]].append(x)
        else:
            combo.update({x[1]:x})

    for x in combo:
        if combo[x][2] == 'GOPT':

        print(x, combo[x])


    #for x in [f for f in object_events if f[2]=='GOPT']:
    '''




#def split_by_indx(alist, indx):
#    return [alist[i:j] for i,j in zip([0]+indx, indx+[None])]

def print_events_of_object(object_name, events):
    event_print = {'PERF':perf_print, 'WLTA':wlta_print, 'WUGR':wugr_print, 'PLIM':plim_print, 'PROD':prod_print}
    keyword_list = ['PERF','WLTA','WUGR','PLIM','PROD','INJE','BHPT','THPT','WEFA','LTAB','GOPT','GWIT','GPLI','GWRT','PERF']

    splitted_events = [] 
    obj_date_keywords = {}
    for x in events:
        keywords = [word for word in x[1:] if len(word)>3 and word[:4].upper() in keyword_list]
        keywords_index = [x.index(i) for i in keywords]
        s_ev = [x[i:j] for i,j in zip([0]+keywords_index, keywords_index+[None])] # split_by_index

        #s_ev = split_by_indx(x,keywords_index)
        #print(keywords)
        #print(keywords_index)
        #print(object_name, s_ev)
        #print(s_ev)

        for x in s_ev[1:]:
            #splitted_events.update({ (s_ev[0][0],x[0][:4].upper()): x[1:] })
            #splitted_events.append((s_ev[0][0], x[0][:4].upper(), x[1:]))
            #print((object_name, s_ev[0][0], x[0][:4].upper(), x[1:]))

            # make  list of all keywords
            # TODO remove duplicate keywords (by date and keyword) and leave the last
            curr_ev = [object_name, s_ev[0][0], x[0][:4].upper(), x[1:]] # all keywords
            if curr_ev not in splitted_events:
                splitted_events.append(curr_ev)

            #pass



    #schedule_events = {}
    #for x in splitted_events:
    #    print(x)

    #unload_perf(splitted_events)
    #unload_gconprod(splitted_events)

    
    #TODO make list of event objects (class Object(field, well, group) and it will have events (name, date))
    #       print events for an object only after treating all it's events





def read_more_events_file(file_name):
    with open(file_name, 'r') as input_file:
        all_events = [x for x in [line.split() for line in  [x[:x.index('/')] if '/' in x else x for x in input_file]  ] if len(x)>0 and x[0][:2]!='--'] # trim comments after '/', filter out empty lines and comment lines

        events_by_object = {} 
        for item in all_events: 
            if item[0] in events_by_object.keys():
                events_by_object[item[0]].append([datetime.strptime(item[1],"%d.%m.%Y")]+item[2:])
            else:
                events_by_object.update({item[0]:[[datetime.strptime(item[1],"%d.%m.%Y")]+item[2:]]})

        for item in events_by_object:
            print_events_of_object(item, events_by_object[item])


read_more_events_file(sys.argv[1])
