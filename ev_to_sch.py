import sys
from datetime import datetime


#def convert_event_to_sch_input(record):
#    print(record)
#



#'''
################ try 2 #############
#def unload_perf(object_events):
#    for x in [f for f in object_events if f[2]=='PERF']:
#        perforation_multiplier = float(x[3][4])
#        if perforation_multiplier > 0: 
#            print(f"{x[1]:%d.%m.%Y}\t{x[0]}\t\tPERFORATION\t\t{x[3][0]}\t{x[3][1]}\t{float(x[3][2])*2:.4f}\t{x[3][3]}")
#            if perforation_multiplier != 1:
#                print(f"{x[1]:%d.%m.%Y}\t{x[0]}\t\tCF-MULTIPLIER\t{x[3][0]}\t{x[3][1]}\t{float(x[3][4])}")
#        else:
#            print(f"{x[1]:%d.%m.%Y}\t{x[0]}\t\tSQUEEZE\t\t\t{x[3][0]}\t{x[3][1]}\t{float(x[3][2])*2:.4f}\t{x[3][3]}")
#
#def unload_gconprod(object_events):
#
#    gopt = [x for x in object_events if x[2]=='GOPT']
#    gpli = [x for x in object_events if x[2]=='GPLI']
#    combo = {}
#
#    for x in gopt:
#        if x[1] in combo:
#            combo[x[1]].append(x)
#        else:
#            combo.update({x[1]:x})
#
#    for x in gpli:
#        if x[1] in combo:
#            combo[x[1]].append(x)
#        else:
#            combo.update({x[1]:x})
#
#    for x in combo:
#        if combo[x][2] == 'GOPT':
#
#        print(x, combo[x])
#
#
#    #for x in [f for f in object_events if f[2]=='GOPT']:
#    '''





#def print_events_of_object(object_name, events):
#    event_print = {'PERF':perf_print, 'WLTA':wlta_print, 'WUGR':wugr_print, 'PLIM':plim_print, 'PROD':prod_print}
#    keyword_list = ['PERF','WLTA','WUGR','PLIM','PROD',
#                    'INJE','BHPT','THPT','WEFA','LTAB',
#                    'GOPT','GWIT','GPLI','GWRT','GLPT',
#                    'PERF','DREF','WALQ','WLTA']
#
#    splitted_events = [] 
#    obj_date_keywords = {}
#    for x in events:
#        keywords = [word for word in x[1:] if len(word)>3 and word[:4].upper() in keyword_list]
#        keywords_index = [x.index(i) for i in keywords]
#        s_ev = [x[i:j] for i,j in zip([0]+keywords_index, keywords_index+[None])] # split_by_index
#
#        s_ev = split_by_indx(x,keywords_index)
#        #print(keywords)
#        #print(keywords_index)
#        #print(object_name, s_ev)
#        print(object_name, s_ev[0], s_ev[1:])
#
#        for x in s_ev[1:]:
#            #splitted_events.update({ (s_ev[0][0],x[0][:4].upper()): x[1:] })
#            #splitted_events.append((s_ev[0][0], x[0][:4].upper(), x[1:]))
#            #print((object_name, s_ev[0][0], x[0][:4].upper(), x[1:]))
#
#            # make  list of all keywords
#            # TODO remove duplicate keywords (by date and keyword) and leave the last
#            curr_ev = [object_name, s_ev[0][0], x[0][:4].upper(), x[1:]] # all keywords
#            if curr_ev not in splitted_events:
#                splitted_events.append(curr_ev)
#
#            #pass
#
#    #schedule_events = {}
#    #for x in splitted_events:
#    #    print(x)
#
#    #unload_perf(splitted_events)
#    #unload_gconprod(splitted_events)
#
#    
#    #TODO make list of event objects (class Object(field, well, group) and it will have events (name, date))
#    #       print events for an object only after treating all it's events












def split_by_indx(alist, indx):
    return [alist[i:j] for i,j in zip([0]+indx, indx+[None])]

def separate(events):
    keyword_list = ['PERF','WLTA','WUGR','PLIM','PROD',
                    'INJE','BHPT','THPT','WEFA','LTAB',
                    'GOPT','GWIT','GPLI','GWRT','GLPT',
                    'PERF','DREF','WALQ','WLTA']

    separated_events = [] 
    obj_date_keywords = {}


    keywords = [word for word in events[1:] if len(word)>3 and word[:4].upper() in keyword_list]
    keywords_index = [events.index(i) for i in keywords]
    s_ev = [events[i:j] for i,j in zip([0]+keywords_index, keywords_index+[None])] # split_by_index
    s_ev = split_by_indx(events,keywords_index)



    for x in s_ev[1:]:
        curr_ev = [ s_ev[0][0], x[0][:4].upper(), x[1:]]
        if curr_ev not in separated_events:
            separated_events.append(curr_ev)

    return separated_events




def perf_print(object_name, event):

    out_string = ''
    date = f'{event[0]:%d.%m.%Y}'
    top = event[2][0]
    bot = event[2][1]
    diameter = 2*float(event[2][2])
    skin = event[2][3]
    multiplier = float(event[2][4])

    if multiplier > 0: 
        out_string =  f"{date}\t{object_name}\tPerforation\t{top}\t{bot}\t{diameter:.4f}\t{skin}"
        if multiplier != 1:
            out_string += f"\n{date}\t{object_name}\tCF-MULTIPLIER\t{top}\t{bot}\t{multiplier}"
    else:
        out_string = f"{date}\t{object_name}\tSqueeze\t{top}\t{bot}\t{diameter:.4f}\t{skin}"

    return out_string


def wlta_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    wlta_modifier = event[2][0]
    return f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WVFPDP\n\t{wlta_modifier}\n"


def wugr_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    wugr_value = event[2][0]
    out_string =  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WGRUPCON\n\tYES\t{wugr_value}\tLIQ\n"

    if len(event[2]) >= 2 and event[2][1].upper() == 'OFF':
        out_string =  f"WELLNAME\t{object_name}\n\t{event[0]:%d.%m.%Y}\tKEYWORD WGRUPCON\n\tNO\n"

    return out_string 


def plim_print(object_name, event):  #### only for WCT !!!!

    date = f'{event[0]:%d.%m.%Y}'
    wcut = event[2][1]

    return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WECON\n\t2* {wcut} 2* WELL\n"


def prod_print(object_name, event): #### !!! Hardcoded first BHP, no THP and VFP table, must be updated by WELTARG BHP !!!

    date = f'{event[0]:%d.%m.%Y}'
    regime = event[2][0]
    rate = event[2][1]
    bhp = 100 # !!!



    #out_string = '--hist prod event'
    out_string = ''

    if regime != 'HLIQ':
        out_string = f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WCONPROD\n\t1* BHP 1* 1* 1* {rate} 1* {bhp}\n"
        if object_name[0] != 'F': # hardcoded FW !!
            out_string += f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WTEST\n\t30 PGE 200 1*\n"

    return out_string


def inje_print(object_name, event): #### !!! Hardcoded firs BHP, THP, no VFP table number

    date = f'{event[0]:%d.%m.%Y}'
    regime = event[2][0]
    rate = event[2][1]
    bhp = 430
    thp = 130
    vfp = ''

    #out_string = '--hist inje event'
    out_string = ''

    if regime != 'HWAT':
        out_string = f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WCONINJE\n\tWATER 1* RATE {rate} 1* {bhp} {thp} {vfp}\n"

    return out_string


def bhpt_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    bhp_target = event[2][0]

    return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tBHP {bhp_target}\n"


# TODO add VFP target to every THP event !!
def thpt_print(object_name, event, vfp_state): #### Beware! It's only for forecast wells !!!!

    date_time = event[0]
    date = f'{event[0]:%d.%m.%Y}'
    thp_target = event[2][0]

    out =  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tTHP {thp_target}\n"
    #out =  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tTHP" # {thp_target}\n"
    vfp_out = ''

    for vfp in vfp_state:
        if date_time < vfp[0]:
            #print(f"vfp state = {vfp[0]}  {vfp[2]}  THP date = {date} NO THP POSSIBLE!")
            return  ''
            
            
        elif date_time >= vfp[0] and len(vfp[2]) > 1:
            if vfp[2][1] == 'OFF':
                #print(f"vfp state = {vfp[0]}  {vfp[2]}  THP date = {date} VFP OFF, NO THP POSSIBLE!")
                ltab_name = vfp[2][0].replace('tubeprod','').replace('tubeinje','')
                return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tVFP 0\n"

        else:
            #print(f"vfp state = {vfp[0]}  {vfp[2]}  THP date = {date} VFP ON")
            ltab_name = vfp[2][0].replace('tubeprod','').replace('tubeinje','')
            vfp_out = f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tVFP {ltab_name}\n"


    #return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tTHP {thp_target}\n"
    return  vfp_out + out


def wefa_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    wefac = event[2][0]
    
    return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WEFAC\n\t{wefac}\n"


def ltab_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    ltab_name = event[2][0].replace('tubeprod','').replace('tubeinje','')
    off = len(event[2]) > 1 and event[2][1] == 'OFF'

    if off:
        return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tVFP 0\n"
    else:
        return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tVFP {ltab_name}\n"



def glpt_print(object_name, event): # !!! made only for FW wells !!!!

    date = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]

    return f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GCONPROD\n\tLRAT 1* 1* 1* {rate} 'NONE'\n"


def gopt_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]
    water_lim = '1*'   ## default value hardcoded !!! check if it updated by GRUPTARG
    off = event[2][1] == 'OFF'

    out_string = f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GCONPROD\n\tORAT {rate} {water_lim} 2* RATE 3* WELL\n"
    if off:
        out_string = f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GCONPROD\n\tFLD\n"

    return out_string


def gpli_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    rate = event[2][1] 
    off = len(event[2]) > 1 and event[2][1] == 'OFF'

    if off:
        return  f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GRUPTARG\n\tWRAT 1*\n"
    else:
        return  f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GRUPTARG\n\tWRAT {rate}\n"



def gwit_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]
    off = len(event[2]) > 1 and event[2][1] == 'OFF'

    if off:
        return  f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GCONINJE\n\tWATER NONE \n"
    else:
        return  f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GCONINJE\n\tWATER RATE {rate}\n"




def gwrt_print(object_name, event): # !!! Hardcoded event !!!

    date = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]
    reinj_frac = 1.0
    #if float(rate) > 6095:
    #    reinj_name = 'GU_CPF2'

    return  f"GROUPNAME\t{object_name}\n\t{date}\tKEYWORD GCONINJE\n\tWATER REIN 1* 1* {reinj_frac} 4* WQ2  \n"




def dref_print(object_name, event, fpd): ### !! NO WHEDREF can't be read by SCHEDULE - make manually 

    date = f'{fpd:%d.%m.%Y}'
    dref = event[2][0]

    return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WHEDREF\n\t{dref}\n"


def walq_print(object_name, event):

    date = f'{event[0]:%d.%m.%Y}'
    walq = event[2][0]

    return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELTARG\n\tLIFT {walq}\n"


def welopen_print(object_name, event):

    out = ''
    date = f'{event[0]:%d.%m.%Y}'

    #return  f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WELOPEN\n\tSHUT\n"
    if event[0] > datetime.datetime(2020, 5, 2, 0, 0):
        out = f"WELLNAME\t{object_name}\n\t{date}\tKEYWORD WCONPROD\n\t1* BHP 1* 1* 1* 0.001 1* 100\n"

    return out

printer = {
        'PERF': perf_print,
        'WLTA': wlta_print,
        'WUGR': wugr_print,
        'PLIM': plim_print,
        'PROD': prod_print,
        'INJE': inje_print,
        'BHPT': bhpt_print,
        'THPT': thpt_print,
        'WEFA': wefa_print,
        'LTAB': ltab_print,
        'GOPT': gopt_print,
        'GWIT': gwit_print,
        'GPLI': gpli_print,
        'GWRT': gwrt_print,
        'GLPT': glpt_print,
        'DREF': dref_print,
        'WALQ': walq_print,
        'WELOPEN': welopen_print
        }


def  eventstring_for_sch(object_name, event, event_printer, fpd = []):
    if len(fpd) > 0:
        return event_printer(object_name, event, fpd)
    else:
        return event_printer(object_name, event)



def read_more_events_file(file_name):
    with open(file_name, 'r') as input_file:
        all_events = [x for x in [line.split() for line in  [x[:x.index('/')] if '/' in x else x for x in input_file]  ] if len(x)>0 and x[0][:2]!='--'] # trim comments after '/', filter out empty lines and comment lines

        # reads events from ev file
        events_by_object = {} 
        for item in all_events: 
            if item[0] in events_by_object.keys():
                events_by_object[item[0]].append([datetime.strptime(item[1],"%d.%m.%Y")]+item[2:])
            else:
                events_by_object.update({item[0]:[[datetime.strptime(item[1],"%d.%m.%Y")]+item[2:]]})


        # pick all event keyword and make separate event for each one
        events_by_object_separated = {}
        for item in events_by_object:

            if item not in events_by_object_separated:
                events_by_object_separated.update({item:[]})

            for event in events_by_object[item]:
                for x in separate(event):
                    events_by_object_separated[item].append(x)
                    #print(x)


        # iterates over all events for all items (well, groups)
        # first loop prints perforations only
        for item in events_by_object_separated:

            for event in events_by_object_separated[item]:
                event_keyword = event[1]
                if event_keyword == 'PERF':
                    print(eventstring_for_sch(item, event, printer[event_keyword]))
 

        print()

        # TODO events analizer (1 - PROD and PERF  for forecast must be at the same date! Or set low rate after PERF (better) )
        # TODO events analizer (2 - THP must always have VFP event )

        # second loop prints all other events
        for item in events_by_object_separated:

            #perf_dates = [x[0] for x in events_by_object_separated[item] if x[1] == 'PERF']
            #if len(perf_dates) > 0:
            #    first_perf_date = perf_dates[0]

            vfp_states = [x  for x in events_by_object_separated[item] if x[1] == 'LTAB']

            for event in events_by_object_separated[item]:
                event_keyword = event[1]

                if event_keyword == 'PERF': # WELOPEN
                    print(eventstring_for_sch(item, event, printer['WELOPEN']))

                if event_keyword not in ['PERF', 'DREF', 'THPT']: 
                    print(eventstring_for_sch(item, event, printer[event_keyword]))

                if event_keyword == 'THPT':
                    print(eventstring_for_sch(item, event, printer[event_keyword], fpd=vfp_states))


                #if event_keyword in ['DREF']:
                #    print(eventstring_for_sch(item, event, printer[event_keyword], fpd=first_perf_date))



read_more_events_file(sys.argv[1])
