import math


def removelanes(projJ):
    old_trackdata = projJ['trackdata']
    old_trackordering = projJ['trackordering']
    new_trackdata = {}
    new_trackordering = []

    for trackid in old_trackordering:
        if trackid in old_trackdata:
            lr_t_trdata = old_trackdata[trackid]
            if 'laned' in lr_t_trdata:
                lr_t_lanedata = lr_t_trdata['lanedata']
                lr_t_laneordering = lr_t_trdata['laneordering']
                if len(lr_t_laneordering) != 0:
                    trackbase = lr_t_trdata.copy()
                    del trackbase['laned']
                    del trackbase['lanedata']
                    del trackbase['laneordering']
                    for laneid in lr_t_laneordering:
                        lr_t_l_data = lr_t_lanedata[laneid]
                        splitnameid = trackid+'_Lane'+laneid
                        if 'placements' in lr_t_l_data: lr_t_l_placements = lr_t_l_data['placements']
                        else: lr_t_l_placements = []

                        if 'name' in lr_t_l_data: lr_t_l_name = lr_t_l_data['name']
                        else: lr_t_l_name = None

                        if 'name' in lr_t_trdata and lr_t_l_name != None: 
                            ntp_name = lr_t_trdata['name']+' ['+lr_t_l_name+']'
                        if 'name' in lr_t_trdata and lr_t_l_name == None: 
                            ntp_name = lr_t_trdata['name']

                        if 'name' not in lr_t_trdata and lr_t_l_name != None: 
                            ntp_name = 'none'+' ['+lr_t_l_name+']'
                        if 'name' not in lr_t_trdata and lr_t_l_name == None: 
                            ntp_name = 'none'

                        part_track_data = trackbase.copy()
                        part_track_data['name'] = ntp_name
                        part_track_data['placements'] = lr_t_l_placements

                        if 'color' not in part_track_data and 'color' in lr_t_l_data:
                            part_track_data['color'] = lr_t_l_data['color']

                        new_trackdata[splitnameid] = part_track_data
                        new_trackordering.append(splitnameid)
                else:
                    new_trackdata[trackid] = lr_t_trdata
                    new_trackordering.append(trackid)
            else:
                new_trackdata[trackid] = lr_t_trdata
                new_trackordering.append(trackid)
    projJ['trackdata'] = new_trackdata
    projJ['trackordering'] = new_trackordering

def get_timesig(patternLength, notesPerBeat):
    MaxFactor = 1024
    factor = 1
    while (((patternLength * factor) % notesPerBeat) != 0 and factor <= MaxFactor):
        factor *= 2
    foundValidFactor = ((patternLength * factor) % notesPerBeat) == 0
    numer = 4
    denom = 4

    if foundValidFactor == True:
        numer = patternLength * factor / notesPerBeat
        denom = 4 * factor
    else: 
        print('Error computing valid time signature, defaulting to 4/4.')

    return [int(numer), denom]


def resize_nl(placementdata):
    in_pos = placementdata['position']
    in_dur = placementdata['duration']

    if 'notelist' in placementdata:
        if placementdata['notelist'] != []:
            in_nl = placementdata['notelist']
            duration_final = None
            for note in in_nl:
                notepos = note['position']
                if duration_final != None:
                    if duration_final > notepos: duration_final = notepos
                else: duration_final = notepos

            if duration_final != 0:
                placementdata['cut'] = {}
                placementdata['cut']['type'] = 'cut'
                placementdata['cut']['start'] = duration_final
                placementdata['cut']['end'] = in_dur

            placementdata['position'] = in_pos+duration_final
    return placementdata


def make_timemarkers(timesig, PatternLengthList, LoopPos):
    prevtimesig = timesig
    timemarkers = []
    currentpos = 0
    blockcount = 0
    for PatternLengthPart in PatternLengthList:
        temptimesig = get_timesig(PatternLengthPart, timesig[1])
        if prevtimesig != temptimesig:
            timemarker = {}
            timemarker['position'] = currentpos
            timemarker['name'] = str(temptimesig[0])+'/'+str(temptimesig[1])
            timemarker['type'] = 'timesig'
            timemarker['numerator'] = temptimesig[0]
            timemarker['denominator'] = temptimesig[1]
            timemarkers.append(timemarker)
        if LoopPos == blockcount:
            timemarker = {}
            if prevtimesig != temptimesig:
                timemarker['name'] = str(temptimesig[0])+'/'+str(temptimesig[1]) + " & Loop"
            else:
                timemarker['name'] = "Loop"
            timemarker['position'] = currentpos
            timemarker['type'] = 'loop'
            timemarkers.append(timemarker)
        prevtimesig = temptimesig
        currentpos += PatternLengthPart
        blockcount += 1
    return timemarkers