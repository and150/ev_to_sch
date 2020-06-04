import sys
from datetime import datetime

SOP = datetime(2020,5,1) # start of prediction


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
    date_string = f'{event[0]:%d.%m.%Y}'
    top = event[2][0]
    bot = event[2][1]
    diameter = 2*float(event[2][2])
    skin = event[2][3]
    multiplier = float(event[2][4])

    if multiplier > 0: 
        out_string =  f"{date_string}\t{object_name}\tPerforation\t{top}\t{bot}\t{diameter:.4f}\t{skin}"
        if multiplier != 1:
            out_string += f"\n{date_string}\t{object_name}\tCF-MULTIPLIER\t{top}\t{bot}\t{multiplier}"
    else:
        out_string = f"{date_string}\t{object_name}\tSqueeze\t{top}\t{bot}\t{diameter:.4f}\t{skin}"

    return out_string


def wlta_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    wlta_modifier = event[2][0]
    return f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WVFPDP\n\t{wlta_modifier}\n"


def wugr_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    wugr_value = event[2][0]
    out_string =  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WGRUPCON\n\tYES\t{wugr_value}\tLIQ\n"

    if len(event[2]) >= 2 and event[2][1].upper() == 'OFF':
        out_string =  f"WELLNAME\t{object_name}\n\t{event[0]:%d.%m.%Y}\tKEYWORD WGRUPCON\n\tNO\n"

    return out_string 


def plim_print(object_name, event):  #### only for WCT !!!!

    date_string = f'{event[0]:%d.%m.%Y}'
    wcut = event[2][1]

    return  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WECON\n\t2* {wcut} 2* WELL\n"


def prod_print(object_name, event, *args): #### !!! Hardcoded first BHP, no THP and VFP table, must be updated by WELTARG BHP !!!

    out_string = ''
    date_string = f'{event[0]:%d.%m.%Y}'
    regime = event[2][0]
    rate = event[2][1]
    bhp = 100 # !!!


    # get current vfp status
    vfp_numb = '0' # default start value
    if len(args)>0:

        vfp_state = args[0]
        for item in vfp_state:
            date = item[0]
            if event[0] >= date:
                vfp_numb = item[2][0].replace('tubeprod','').replace('tubeinje','')

                if len(item[2])>1:
                    if item[2][1] == 'OFF':
                        vfp_numb = '0'
            #print(date, vfp_numb, event[0]) # debug print



    if regime != 'HLIQ':
        out_string = f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WCONPROD\n\t1* BHP 1* 1* 1* {rate} 1* {bhp} 1* {vfp_numb}\n"
        if object_name[0] != 'F': # hardcoded FW !!
            out_string += f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WTEST\n\t30 PGE 200 1*\n"
    else:
        out_string = f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD VFP\n\t{vfp_numb}\n"

    return out_string


def inje_print(object_name, event, *args): #### !!! Hardcoded firs BHP, THP, no VFP table number

    out_string = ''
    date_string = f'{event[0]:%d.%m.%Y}'
    regime = event[2][0]
    rate = event[2][1]
    bhp = 430
    thp = 130

    # get current vfp status
    vfp_numb = '0' # default start value
    if len(args)>0:

        vfp_state = args[0]
        for item in vfp_state:
            date = item[0]
            if event[0] >= date:
                vfp_numb = item[2][0].replace('tubeprod','').replace('tubeinje','')

                if len(item[2])>1:
                    if item[2][1] == 'OFF':
                        vfp_numb = '0'
            #print(date, vfp_numb, event[0]) # debug print

    if regime != 'HWAT':
        out_string = f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WCONINJE\n\tWATER 1* RATE {rate} 1* {bhp} {thp} {vfp_numb}\n"
    else:
        pass

    return out_string


def bhpt_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    bhp_target = event[2][0]

    return  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WELTARG\n\tBHP {bhp_target}\n"


def thpt_print(object_name, event, *args):

    date_string = f'{event[0]:%d.%m.%Y}'
    thp_target = event[2][0]

    out_string =  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WELTARG\n\tTHP {thp_target}\n"

    # get current vfp status
    vfp_numb = '0' # default start value
    if len(args)>0:

        vfp_state = args[0]
        for item in vfp_state:
            date = item[0]
            if event[0] >= date:
                vfp_numb = item[2][0].replace('tubeprod','').replace('tubeinje','')

                if len(item[2])>1:
                    if item[2][1] == 'OFF':
                        vfp_numb = '0'
            #print(date, vfp_numb, event[0]) # debug print

    if vfp_numb == '0':
        out_string =  '' 

    return out_string 


def wefa_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    wefac = event[2][0]
    
    return  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WEFAC\n\t{wefac}\n"


def ltab_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    ltab_name = event[2][0].replace('tubeprod','').replace('tubeinje','')
    off = len(event[2]) > 1 and event[2][1] == 'OFF'

    if off:
        return  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WELTARG\n\tVFP 0\n"
    else:
        return  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WELTARG\n\tVFP {ltab_name}\n"



def glpt_print(object_name, event): # !!! made only for FW wells !!!!

    date_string = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]

    return f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GCONPROD\n\tLRAT 1* 1* 1* {rate} 'NONE'\n"


def gopt_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]
    water_lim = '1*'   ## default value hardcoded !!! check if it updated by GRUPTARG
    off = event[2][1] == 'OFF'

    out_string = f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GCONPROD\n\tORAT {rate} {water_lim} 2* RATE 3* WELL\n"
    if off:
        out_string = f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GCONPROD\n\tFLD\n"

    return out_string


def gpli_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    rate = event[2][1] 
    off = len(event[2]) > 1 and event[2][1] == 'OFF'

    if off:
        return  f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GRUPTARG\n\tWRAT 1*\n"
    else:
        return  f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GRUPTARG\n\tWRAT {rate}\n"


def gwit_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]
    off = len(event[2]) > 1 and event[2][1] == 'OFF'

    if off:
        return  f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GCONINJE\n\tWATER NONE \n"
    else:
        return  f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GCONINJE\n\tWATER RATE {rate}\n"


def gwrt_print(object_name, event): # !!! Hardcoded event !!!

    date_string = f'{event[0]:%d.%m.%Y}'
    rate = event[2][0]
    reinj_frac = 1.0
    #if float(rate) > 6095:
    #    reinj_name = 'GU_CPF2'

    return  f"GROUPNAME\t{object_name}\n\t{date_string}\tKEYWORD GCONINJE\n\tWATER REIN 1* 1* {reinj_frac} 4* WQ2\n"


def dref_print(object_name, event, fpd): ### !! NO WHEDREF can't be read by SCHEDULE - make manually 

    date_string = f'{fpd:%d.%m.%Y}'
    dref = event[2][0]

    return  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WHEDREF\n\t{dref}\n"


def walq_print(object_name, event):

    date_string = f'{event[0]:%d.%m.%Y}'
    walq = event[2][0]

    return  f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WELTARG\n\tLIFT {walq}\n"


def welopen_print(object_name, event):

    out = ''
    date_string = f'{event[0]:%d.%m.%Y}'

    if event[0] > SOP:
        out = f"WELLNAME\t{object_name}\n\t{date_string}\tKEYWORD WCONPROD\n\t1* BHP 1* 1* 1* 0.0  1* 100\n"

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


def  eventstring_for_sch(object_name, event, event_printer, *args):
    return event_printer(object_name, event, *args)
    #if len(fpd) > 0:
    #    return event_printer(object_name, event, fpd)
    #else:
    #    return event_printer(object_name, event)



def read_more_events_file(file_name):

    events_by_object_separated = {}

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
        for item in events_by_object:

            if item not in events_by_object_separated:
                events_by_object_separated.update({item:[]})

            for event in events_by_object[item]:
                for x in separate(event):
                    events_by_object_separated[item].append(x)
                    #print(x)

    return events_by_object_separated




def print_sch_input(events_by_object_separated):

        #the first loop prints PERForations only
        for item in events_by_object_separated:
            for event in events_by_object_separated[item]:
                event_keyword = event[1]
                if event_keyword == 'PERF':
                    print(eventstring_for_sch(item, event, printer[event_keyword]))
        print()

        #the second loop prints zero limits after SOP
        for item in events_by_object_separated:
            for event in events_by_object_separated[item]:
                event_keyword = event[1]
                event_date = event[0]
                if event_keyword == 'PERF' and event_date > SOP:
                    print(eventstring_for_sch(item, event, printer['WELOPEN']))
                    break # ???
        print()

        # TODO make printer of DREF (it doesn't work? need to check again) !!!
        # TODO change GCONPROD (the water limit need to be combined with the oil limit)
        #the third loop prints all other events
        for item in events_by_object_separated:

            #perf_dates = [x[0] for x in events_by_object_separated[item] if x[1] == 'PERF']
            #if len(perf_dates) > 0:
            #    first_perf_date = perf_dates[0]

            vfp_states = [x for x in events_by_object_separated[item] if x[1] == 'LTAB']

            for event in events_by_object_separated[item]:
                event_keyword = event[1]

                if event_keyword not in ['PERF', 'DREF', 'PROD', 'INJE', 'THPT']: #['PERF', 'DREF', 'THPT']: 
                    print(eventstring_for_sch(item, event, printer[event_keyword]))

                if event_keyword in ['PROD', 'INJE', 'THPT']:
                    print(eventstring_for_sch(item, event, printer[event_keyword], vfp_states))





if __name__ == '__main__':

    events = read_more_events_file(sys.argv[1])
    print_sch_input(events)
