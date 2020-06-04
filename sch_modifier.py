import sys

def read_shut_events(events_file_name):
    '''
    Reads: 
        event file with perforations (Tempest format)
        example: "100A	18.02.2031	PERF	27	27	0.108	0	0	ZONE / PERMX = 	4305.72998"

    Return: dictionary {well:[k1,k2,k3...]}
    '''

    connections_to_shut = {}
    ev_gen = (row for row in open(events_file_name))
    for row in ev_gen:
        words = row.split()
        if words!=[]:
            if words[0] in connections_to_shut:
                connections_to_shut[words[0]].append(words[3])
            else:
                connections_to_shut.update({words[0]:[words[3]]})

    #for item in connections_to_shut: print(item,connections_to_shut[item]) # debug print
    return connections_to_shut


def shut_hi_perm_connections(compdat_words, conn_to_shut):
    well_name = compdat_words[0]
    k1 = compdat_words[3]
    k2 = compdat_words[4]

    if k1 != k2:
        print(f"WARNING! K1 != K2 for well {well_name}") # TODO does not work for K1 != K2 !!!
        #TODO function doesn't implement reading default values like 2*, 3*, 4* etc (1* only) !!!!

    if well_name[1:-1] in conn_to_shut:
        if k1 in conn_to_shut[well_name[1:-1]]:
            return compdat_words[:5] + ["'SHUT'"] + compdat_words[6:]

    # default return (no changes)
    return compdat_words



def read_dref_events(events_file_name):
    '''
    Reads: Tempest event file

    Return: dictionary {well: dref}
    '''

    drefs_to_paste = {}
    ev_gen = (row for row in open(events_file_name))
    for row in ev_gen:
        words = row.split()
        if words!=[]:
            if words[0][:2]!='--' and len(words)>2 and words[2].upper()=='DREF':
                drefs_to_paste[words[0]] = words[3]
    return drefs_to_paste


def change_drefs(welspecs_words, drefs_to_paste):
    well_name = welspecs_words[0]

    #TODO function doesn't implement reading default values like 2*, 3*, 4* etc (1* only) !!!!
    if len({'2*','3*','4*','5*'}.intersection(welspecs_words[:6])) > 0:
        print(f"WARNING! default values was not read!!")

    if well_name[1:-1] in drefs_to_paste:
        return welspecs_words[:4] + [drefs_to_paste[well_name[1:-1]]] + welspecs_words[5:]
    else:
        return welspecs_words



def fix_wconinjh(words, *args):
    '''
    Reads: words from a line of WCONINJE section 

    Return: words for a line of WCONINJH section 
    '''
   # change WCONINJE syntax into WCONINJH 
    
    unwrapped = [item for sublist in [['1*']*int(x[0]) if '*' in x else [x] for x in words] for item in sublist] # unwrap eclipse 'N*' syntax ( 3* -> 1* 1* 1*)

    #for x in [['1*']*int(x[0]) if '*' in x else x for x in words]:
    #    if isinstance(x, list):
    #        unwrapped += x
    #    else:
    #        unwrapped += [x]


    del(unwrapped[3]) # remove 'RATE' keyword

    hardcode_press = '430.0'
    if unwrapped[5] == '1*':
        return unwrapped[:4] + unwrapped[5:]
    elif float(unwrapped[5]) == 0.01:
        return unwrapped[:4] + [hardcode_press] + unwrapped[6:]
    else:
        return unwrapped[:4] + unwrapped[5:]





def read_sch_file(sch_file_name, keyword, processing_function, *args):
    '''
    Reads: Eclipse schedule file, filters section Keyword and performs processing_function on it 

    Return: Prints Eclipse schedule file with modified Keyword section 
    '''

    sch_gen = (row for row in open(sch_file_name))

    isKeyword = False 
    for row in sch_gen:
        words = row.split()

        if words == [] or words[0][:1] == '--':
            print(row.rstrip())
            continue

        if words!=[] and words[0] == '/':
            isKeyword = False

        # work here
        if isKeyword:
            #print(isKeyword, words)
            #print(*processing_function(words, args)) # shut hi perm intervals in COMPDAT
            #print(*processing_function(words, args)) # change Drefs in WELSPECS
            print(*processing_function(words, args)) # fix WCONINJH
        else:
            print(row.rstrip())


        if words!=[] and words[0] == keyword:
            isKeyword = True





if __name__ == '__main__':
    #conn_to_shut = read_shut_events(sys.argv[1])
    #read_sch_file(sys.argv[2],'COMPDAT', shut_hi_perm_connections, conn_to_shut)

    #drefs_to_paste = read_dref_events(sys.argv[1])
    #read_sch_file(sys.argv[2], 'WELSPECS', drefs_to_paste, change_drefs)

    read_sch_file(sys.argv[1], 'WCONINJH', fix_wconinjh)
