# SPDX-FileCopyrightText: 2023 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import plugin_output
import json
import io
import os
import zipfile
import math
import lxml.etree as ET
from functions import placements
from functions import plugins
from functions import data_values
from functions import params
from functions import audio
from functions import auto
from functions import notelist_data
from functions import song
from functions import xtramath
from functions_plugin import synth_nonfree_values
from functions_tracks import auto_nopl
from functions_tracks import tracks_r

id_out_num = 10000
devid_out_num = 30000
audioidnum = 0

def getid(): 
    global id_out_num
    id_out_num += 1
    return id_out_num

def device_getid(): 
    global devid_out_num
    devid_out_num += 1
    return devid_out_num

def addsample(zip_amped, filepath): 
    global audioidnum
    global audio_id
    outnum = None
    filebasename = os.path.basename(filepath)
    if filebasename not in audio_id:
        audio_id[filebasename] = audioidnum
        if os.path.exists(filepath):
            filetype = filebasename.split('.')[1]
            if filetype in ['wav']: zip_amped.write(filepath, str(audioidnum))
            else: zip_amped.writestr(str(audioidnum), audio.convert_to_wav(filepath))
            outnum = audioidnum
            audioidnum += 1
    else:
        outnum = audio_id[filebasename]
    return outnum

def amped_maketrack(): 
    amped_trackdata = {}
    amped_trackdata["id"] = getid()
    amped_trackdata["name"] = ""
    amped_trackdata["color"] = "mint"
    amped_trackdata["pan"] = 0
    amped_trackdata["volume"] = 1
    amped_trackdata["mute"] = False
    amped_trackdata["solo"] = False
    amped_trackdata["armed"] = {"mic": False, "keys": False}
    amped_trackdata["regions"] = []
    amped_trackdata["devices"] = []
    amped_trackdata["automations"] = []
    return amped_trackdata

def amped_makeregion(position, duration, offset): 
    amped_region = {}
    amped_region["id"] = getid()
    amped_region["position"] = position/4
    amped_region["length"] = duration/4
    amped_region["offset"] = offset/4
    amped_region["loop"] = 0
    amped_region["clips"] = []
    amped_region["midi"] = {"notes": [], "events": [], "chords": []}
    amped_region["name"] = ""
    amped_region["color"] = "mint"
    return amped_region

def amped_makedevice(className, label): 
    amped_device = {}
    amped_device["id"] = device_getid()
    amped_device["className"] = className
    amped_device["label"] = label
    amped_device["params"] = []
    amped_device["preset"] = {}
    amped_device["bypass"] = False
    return amped_device

def do_idparams(pluginid):
    paramout = []
    paramlist = plugins.get_plug_paramlist(cvpj_l, pluginid)
    for paramnum in range(len(paramlist)):
        paramdata = plugins.get_plug_param(cvpj_l, pluginid, paramlist[paramnum], 0)
        paramout.append({"id": paramnum, "name": paramdata[2], "value": paramdata[0]})
    return paramout

def amped_parse_effects(fxchain_audio):
    outdata = []
    for pluginid in fxchain_audio:
        plugtype = plugins.get_plug_type(cvpj_l, pluginid)
        fxdata = data_values.nested_dict_get_value(cvpj_l, ['plugins', pluginid])
        fx_on, fx_wet = plugins.get_plug_fxdata(cvpj_l, pluginid)

        fx_on = not fx_on

        if plugtype[0] == 'universal' and plugtype[1] in ['compressor', 'expander']:
            device_params = []

            preGainDB = plugins.get_plug_param(cvpj_l, pluginid, 'pregain', 0)[0]
            ratio = plugins.get_plug_param(cvpj_l, pluginid, 'ratio', 0)[0]
            thresholdDB = plugins.get_plug_param(cvpj_l, pluginid, 'threshold', 0)[0]
            attackTimeMS = plugins.get_plug_param(cvpj_l, pluginid, 'attack', 0)[0]*1000
            releaseTimeMS = plugins.get_plug_param(cvpj_l, pluginid, 'release', 0)[0]*1000
            postGainDB = plugins.get_plug_param(cvpj_l, pluginid, 'postgain', 0)[0]
            lookaheadTimeMS = plugins.get_plug_param(cvpj_l, pluginid, 'lookahead', 0)[0]*1000
            softKneeWidth = plugins.get_plug_param(cvpj_l, pluginid, 'knee', 0)[0]/6

            detect_mode = plugins.get_plug_dataval(cvpj_l, pluginid, 'detect_mode', 'rms')
            circuit_mode = plugins.get_plug_dataval(cvpj_l, pluginid, 'circuit_mode', 'digital')

            detectMode = 1
            if detect_mode == 'peak': detectMode = 0

            circuitMode = 1
            if detect_mode == 'analog': detectMode = 0

            filt_enabled, filt_cutoff, filt_reso, filt_type, filt_subtype = plugins.get_filter(cvpj_l, pluginid)

            filterMode = 0
            if filt_type == 'lowpass': filterMode = 0
            if filt_type == 'highpass': filterMode = 1
            if filt_type == 'bandpass': filterMode = 2

            filterFrequency = filt_cutoff
            filterQ = filt_reso
            filterGainDB = plugins.get_plug_dataval(cvpj_l, pluginid, 'filter_gain', 0)
            filterActive = int(filt_enabled)
            filterAudition = 0

            device_params.append({'id': 0, 'name': 'preGainDB', 'value': preGainDB})
            device_params.append({'id': 8, 'name': 'ratio', 'value': ratio})
            device_params.append({'id': 5, 'name': 'thresholdDB', 'value': thresholdDB})
            device_params.append({'id': 2, 'name': 'attackTimeMS', 'value': attackTimeMS})
            device_params.append({'id': 3, 'name': 'releaseTimeMS', 'value': releaseTimeMS})
            device_params.append({'id': 1, 'name': 'postGainDB', 'value': postGainDB})
            device_params.append({'id': 4, 'name': 'lookaheadTimeMS', 'value': lookaheadTimeMS})
            device_params.append({'id': 7, 'name': 'softKneeWidth', 'value': softKneeWidth})
            device_params.append({'id': 12, 'name': 'detectMode', 'value': detectMode})
            device_params.append({'id': 13, 'name': 'circuitMode', 'value': circuitMode})
            device_params.append({'id': 14, 'name': 'filterMode', 'value': filterMode})
            device_params.append({'id': 15, 'name': 'filterFrequency', 'value': filterFrequency})
            device_params.append({'id': 16, 'name': 'filterQ', 'value': filterQ})
            device_params.append({'id': 17, 'name': 'filterGainDB', 'value': filterGainDB})
            device_params.append({'id': 18, 'name': 'filterActive', 'value': filterActive})
            device_params.append({'id': 19, 'name': 'filterAudition', 'value': filterAudition})

            if plugtype[1] == 'compressor': devicedata = amped_makedevice('Compressor', 'Compressor')
            if plugtype[1] == 'expander': devicedata = amped_makedevice('Expander', 'Expander')
            
            devicedata['bypass'] = fx_on
            devicedata['params'] = device_params
            outdata.append(devicedata)

        elif plugtype == ['universal', 'delay-c']:
            d_time_type = plugins.get_plug_dataval(cvpj_l, pluginid, 'time_type', 'seconds')
            d_time = plugins.get_plug_dataval(cvpj_l, pluginid, 'time', 1)
            d_wet = plugins.get_plug_dataval(cvpj_l, pluginid, 'wet', fx_wet)
            d_feedback = plugins.get_plug_dataval(cvpj_l, pluginid, 'feedback', 0.0)
            devicedata = amped_makedevice('Delay', 'Delay')

            device_params = []
            if d_time_type == 'seconds':
                device_params.append({'id': 0, 'name': 'time', 'value': d_time})

            if d_time_type == 'steps':
                device_params.append({'id': 0, 'name': 'time', 'value': (d_time/8)*((amped_bpm)/120) })

            device_params.append({'id': 1, 'name': 'fb', 'value': d_feedback})
            device_params.append({'id': 2, 'name': 'mix', 'value': d_wet})
            device_params.append({'id': 3, 'name': 'damp', 'value': 0})
            device_params.append({'id': 4, 'name': 'cross', 'value': 0})
            device_params.append({'id': 5, 'name': 'offset', 'value': 0})
            devicedata['bypass'] = fx_on
            devicedata['params'] = device_params
            outdata.append(devicedata)

        elif plugtype == ['universal', 'eq-bands']:
            devicedata = amped_makedevice('EqualizerPro', 'Equalizer')
            devicedata['bypass'] = fx_on
            out_params = []

            banddata = plugins.get_eqband(cvpj_l, pluginid, None)

            paramnum = 0

            for num in range(min(len(banddata),8)):

                eqnumtxt = str(num+1)
                s_band = banddata[num]

                band_type = s_band['type']
                band_on = float(s_band['on'])
                band_freq = s_band['freq']
                band_gain = s_band['gain']
                band_res = s_band['var']

                filtername = "filter/"+eqnumtxt+"/"

                eq_bandtype = 0
                if band_type == 'peak': eq_bandtype = 0
                if band_type == 'low_pass': eq_bandtype = 2
                if band_type == 'high_pass': eq_bandtype = 1
                if band_type == 'low_shelf': eq_bandtype = 3
                if band_type == 'high_shelf': eq_bandtype = 4

                if band_type in ['low_pass', 'high_pass']: 
                    band_res = xtramath.logpowmul(band_res, 0.5) if band_res != 0 else band_res
                if band_type in ['low_pass', 'peak']: 
                    band_res = xtramath.logpowmul(band_res, -1) if band_res != 0 else band_res

                out_params.append({"id": paramnum, "name": filtername+'active', "value": band_on})
                out_params.append({"id": paramnum+1, "name": filtername+'freq', "value": band_freq})
                out_params.append({"id": paramnum+2, "name": filtername+'gain', "value": band_gain})
                out_params.append({"id": paramnum+3, "name": filtername+'type', "value": eq_bandtype})
                out_params.append({"id": paramnum+4, "name": filtername+'q', "value": band_res})

                paramnum += 5

            postGain = plugins.get_plug_param(cvpj_l, pluginid, 'gain_out', 0)[0]

            out_params.append({"id": paramnum, "name": 'postGain', "value": postGain})
            devicedata['params'] = out_params
            outdata.append(devicedata)

        elif plugtype == ['universal', 'vibrato']:
            d_freq = plugins.get_plug_param(cvpj_l, pluginid, 'freq', 0)[0]
            d_depth = plugins.get_plug_param(cvpj_l, pluginid, 'depth', 0)[0]
            devicedata = amped_makedevice('Vibrato', 'Vibrato')
            devicedata['bypass'] = fx_on
            device_params = []
            device_params.append({'id': 13, 'name': 'delayLfoRateHz', 'value': d_freq})
            device_params.append({'id': 12, 'name': 'delayLfoDepth', 'value': d_depth})
            devicedata['params'] = device_params
            outdata.append(devicedata)

        elif plugtype == ['universal', 'tremolo']:
            d_freq = plugins.get_plug_param(cvpj_l, pluginid, 'freq', 0)[0]
            d_depth = plugins.get_plug_param(cvpj_l, pluginid, 'depth', 0)[0]
            devicedata = amped_makedevice('Tremolo', 'Tremolo')
            devicedata['bypass'] = fx_on
            device_params = []
            device_params.append({'id': 6, 'name': 'lfoARateHz', 'value': d_freq})
            device_params.append({'id': 5, 'name': 'lfoADepth', 'value': d_depth})
            devicedata['params'] = device_params
            outdata.append(devicedata)

        elif plugtype == ['universal', 'bitcrush']:
            b_bits = plugins.get_plug_param(cvpj_l, pluginid, 'bits', 0)[0]
            b_freq = plugins.get_plug_param(cvpj_l, pluginid, 'freq', 0)[0]

            b_freq = (math.log(b_freq / 100) / math.log(2))/10

            devicedata = amped_makedevice('BitCrusher', 'BitCrusher')
            devicedata['bypass'] = fx_on
            device_params = []
            device_params.append({'id': 0, 'name': 'bits', 'value': b_bits})
            device_params.append({'id': 1, 'name': 'down', 'value': b_freq})
            device_params.append({'id': 2, 'name': 'mix', 'value': fx_wet})

            devicedata['params'] = device_params
            outdata.append(devicedata)

        elif plugtype[0] == 'native-amped':

            if plugtype[1] in ["Amp Sim Utility", 'Clean Machine', 'Distortion Machine', 'Metal Machine']:
                devicedata = amped_makedevice('WAM', 'Amp Sim Utility')
                devicedata['bypass'] = fx_on
                if plugtype[1] == "Amp Sim Utility": wamClassName = "WASABI_SC.Utility"
                if plugtype[1] == "Clean Machine": wamClassName = 'WASABI_SC.CleanMachine'
                if plugtype[1] == "Distortion Machine": wamClassName = 'WASABI_SC.DistoMachine'
                if plugtype[1] == "Metal Machine": wamClassName = 'WASABI_SC.MetalMachine'
                devicedata['wamClassName'] = wamClassName
                devicedata['wamPreset'] = plugins.get_plug_dataval(cvpj_l, pluginid, 'data', '{}')
                outdata.append(devicedata)

            elif plugtype[1] in ['BitCrusher', 'Chorus', 
        'CompressorMini', 'Delay', 'Distortion', 'Equalizer', 
        'Flanger', 'Gate', 'Limiter', 'LimiterMini', 'Phaser', 
        'Reverb', 'Tremolo', 'Vibrato', 'Equalizer']:
                classname = plugtype[1]
                classlabel = plugtype[1]
                if classname == 'CompressorMini': classlabel = 'Equalizer Mini'
                if classname == 'Equalizer': classlabel = 'Equalizer Mini'
                if classname == 'LimiterMini': classlabel = 'Limiter Mini'
                if classname == 'EqualizerPro': classlabel = 'Equalizer'
                devicedata = amped_makedevice(classname, classlabel)
                devicedata['bypass'] = fx_on
                devicedata['params'] = do_idparams(pluginid)
                outdata.append(devicedata)

    return outdata

def amped_makeparam(i_id, i_name, i_value):
    return {"id": i_id, "name": i_name, "value": i_value}

def cvpjauto_to_ampedauto(autopoints):
    ampedauto = []
    for autopoint in autopoints:
        ampedauto.append({"pos": autopoint['position']/4, "value": autopoint['value']})
    return ampedauto

class output_cvpj_f(plugin_output.base):
    def __init__(self): pass
    def is_dawvert_plugin(self): return 'output'
    def getname(self): return 'Amped Studio'
    def getshortname(self): return 'amped'
    def gettype(self): return 'r'
    def plugin_archs(self): return None
    def getdawcapabilities(self): 
        return {
        'placement_cut': True,
        'track_hybrid': True,
        'auto_nopl': True,
        'placement_audio_stretch': ['rate']
        }
    def getsupportedplugformats(self): return ['vst2', 'midi']
    def getsupportedplugins(self): return ['sampler:single', 'midi', 'universal:compressor', 'universal:expander']
    def getfileextension(self): return 'zip'
    def parse(self, convproj_json, output_file):
        global audio_id
        global cvpj_l
        global amped_bpm
        global europa_vals

        europa_vals = synth_nonfree_values.europa_valnames()

        cvpj_l = json.loads(convproj_json)
        audio_id = {}

        zip_bio = io.BytesIO()
        zip_amped = zipfile.ZipFile(zip_bio, mode='w', compresslevel=None)

        amped_bpm = int(params.get(cvpj_l, [], 'bpm', 120)[0])
        amped_numerator, amped_denominator = song.get_timesig(cvpj_l)

        amped_tracks = []
        amped_filenames = {}

        for cvpj_trackid, cvpj_trackdata, track_placements in tracks_r.iter(cvpj_l):
            amped_trackdata = amped_maketrack()
            amped_trackdata["name"] = cvpj_trackdata['name'] if 'name' in cvpj_trackdata else ''
            amped_trackdata["pan"] = params.get(cvpj_trackdata, [], 'pan', 0)[0]
            amped_trackdata["volume"] = params.get(cvpj_trackdata, [], 'vol', 1.0)[0]
            amped_trackdata["mute"] = not params.get(cvpj_trackdata, [], 'on', True)[0]
            amped_trackdata["solo"] = bool(params.get(cvpj_trackdata, [], 'solo', False)[0])

            inst_supported = False

            if 'instdata' in cvpj_trackdata:
                cvpj_instadata = cvpj_trackdata['instdata']
                pluginid = cvpj_instadata['pluginid'] if 'pluginid' in cvpj_instadata else None
                if pluginid != None:
                    plugtype = plugins.get_plug_type(cvpj_l, pluginid)

                    if plugtype == ['synth-nonfree', 'Europa']:
                        inst_supported = True
                        europa_data = amped_makedevice('WAM','Europa')
                        europa_data['params'] = []
                        europa_data['bypass'] = False
                        europa_data['wamClassName'] = 'Europa'
                        wamPreset = {}
                        wamPreset['patch'] = 'DawVert'
                        europa_patch = ET.Element("JukeboxPatch")
                        europa_name = ET.SubElement(europa_patch, "DeviceNameInEnglish")
                        europa_name.text = "Europa Shapeshifting Synthesizer"
                        europa_prop = ET.SubElement(europa_patch, "Properties")
                        europa_prop.set('deviceProductID','se.propellerheads.Europa')
                        europa_prop.set('deviceVersion','2.0.0f')
                        europa_obj = ET.SubElement(europa_prop, "Object")
                        europa_obj.set('name','custom_properties')
                        for eur_value_name in europa_vals:
                            eur_value_type, cvpj_val_name = europa_vals[eur_value_name]
                            if eur_value_type == 'number':
                                eur_value_value = plugins.get_plug_param(cvpj_l, pluginid, cvpj_val_name, 0)[0]
                            else:
                                eur_value_value = plugins.get_plug_dataval(cvpj_l, pluginid, cvpj_val_name, 0)
                                if eur_value_name in ['Curve1','Curve2','Curve3','Curve4','Curve']: eur_value_value = bytes(eur_value_value).hex().upper()

                            europa_value_obj = ET.SubElement(europa_obj, "Value")
                            europa_value_obj.set('property',eur_value_name)
                            europa_value_obj.set('type',eur_value_type)
                            europa_value_obj.text = str(eur_value_value)
                        wamPreset['settings'] = ET.tostring(europa_patch).decode()
                        wamPreset['encodedSampleData'] = plugins.get_plug_dataval(cvpj_l, pluginid, 'encodedSampleData', [])

                        europa_data['wamPreset'] = json.dumps(wamPreset)

                        amped_trackdata["devices"].append(europa_data)

                    elif plugtype[0] == 'midi':
                        inst_supported = True
                        midi_bank = plugins.get_plug_dataval(cvpj_l, pluginid, 'bank', 0)
                        midi_patch = plugins.get_plug_dataval(cvpj_l, pluginid, 'inst', 0)
                        sf2data = amped_makedevice('SF2','GM Player')
                        sf2params = []
                        sf2params.append(amped_makeparam(0, 'patch', 0))
                        sf2params.append(amped_makeparam(1, 'bank', midi_bank))
                        sf2params.append(amped_makeparam(2, 'preset', midi_patch))
                        sf2params.append(amped_makeparam(3, 'gain', 0.75))
                        sf2params.append(amped_makeparam(4, 'omni', 1))
                        sf2data['params'] = sf2params
                        sf2data['sf2Preset'] = {"bank": midi_bank, "preset": midi_patch, "name": ""}
                        amped_trackdata["devices"].append(sf2data)

                    elif plugtype == ['vst2', 'win']:
                        inst_supported = True
                        vstcondata = amped_makedevice('VSTConnection',"VST/Remote Beta")
                        vstdatatype = plugins.get_plug_dataval(cvpj_l, pluginid, 'datatype', '')
                        if vstdatatype == 'chunk':
                            vstcondata['pluginPath'] = plugins.get_plug_dataval(cvpj_l, pluginid, 'path', 'path')
                            vstcondata['pluginState'] = plugins.get_plug_dataval(cvpj_l, pluginid, 'chunk', '')
                        amped_trackdata["devices"].append(vstcondata)

            if inst_supported == False:
                sf2data = amped_makedevice('SF2','GM Player')
                sf2params = []
                sf2params.append(amped_makeparam(0, 'patch', 0))
                sf2params.append(amped_makeparam(1, 'bank', 0))
                sf2params.append(amped_makeparam(2, 'preset', 0))
                sf2params.append(amped_makeparam(3, 'gain', 0.75))
                sf2params.append(amped_makeparam(4, 'omni', 1))
                sf2data['params'] = sf2params
                sf2data['sf2Preset'] = {"bank": 0, "preset": 0, "name": ""}
                amped_trackdata["devices"].append(sf2data)

                    #if plugtype == ['sampler', 'single']:
                    #    samplerdata = amped_makedevice('Sampler',"Sampler")
                    #    samplerdata['samplerZones'] = []
                    #    a_predelay, a_attack, a_hold, a_decay, a_sustain, a_release, a_amount = plugins.get_asdr_env(cvpj_l, pluginid, 'vol')

                    #    filepath = plugins.get_plug_dataval(cvpj_l, pluginid, 'file', '')
                    #    audioid = addsample(zip_amped, filepath)

                    #    samplervalues = {}
                    #    samplervalues["voiceLimit"] = 64
                    #    samplervalues["filter/frequencyHz/min"] = 2600
                    #    samplervalues["filter/frequencyHz/max"] = 20000
                    #    samplervalues["filter/resonanceNorm/min"] = 0.35
                    #    samplervalues["filter/resonanceNorm/max"] = 0.67
                    #    samplervalues["eg/0/attackDurationNorm"] = a_attack/10
                    #    samplervalues["eg/0/attackCurve"] = 0
                    #    samplervalues["eg/0/decayDurationNorm"] = a_decay/10
                    #    samplervalues["eg/0/decayCurve"] = 0
                    #    samplervalues["eg/0/sustainLevelNorm"] = a_sustain
                    #    samplervalues["eg/0/releaseCurve"] = 0
                    #    samplervalues["eg/0/releaseDurationNorm"] = a_release/10
                    #    samplervalues["eg/0/tracksVelocity"] = 1
                    #    samplervalues["eg/0/velocityTracker/input/min"] = 0
                    #    samplervalues["eg/0/velocityTracker/input/max"] = 127

                    #    samplervalues["zone/1/key/max"] = 127
                    #    samplervalues["zone/1/key/root"] = 60
                    #    samplervalues["zone/1/key/min"] = 0
                    #    samplervalues["zone/1/velocity/min"] = 0
                    #    samplervalues["zone/1/velocity/max"] = 127
                    #    samplervalues["zone/1/eg/0/velocityTracker/gain/amount"] = 1
                    #    samplervalues["zone/1/looping/mode"] = 0
                    #    samplervalues["zone/1/looping/release"] = 2
                    #    samplervalues["zone/1/looping/startPositionNorm"] = 0
                    #    samplervalues["zone/1/looping/endPositionNorm"] = 1
                    #    samplervalues["zone/1/looping/crossfadeWidthNorm"] = 0
                    #    samplervalues["zone/1/looping/crossfadeCurve"] = 0

                    #    samplerparams = []
                    #    paramnum = 0
                    #    for name in samplervalues: 
                    #        samplerparams.append(amped_makeparam(paramnum, name, samplervalues[name]))
                    #        paramnum += 1

                    #    samplerdata['params'] = samplerparams
                    #    samplercontentGuid = {}
                    #    samplercontentGuid['userAudio'] = {"exportedId": str(audioid)}
                    #    samplerdata['samplerZones'].append({"id": 1, "contentGuid": samplercontentGuid})
                    #    samplerdata['nextZoneId'] = 1
                    #    amped_trackdata["devices"].append(samplerdata)

            if 'notes' in track_placements: 
                cvpj_noteclips = notelist_data.sort(track_placements['notes'])
                for cvpj_noteclip in cvpj_noteclips:
                    amped_position = cvpj_noteclip['position']
                    amped_duration = cvpj_noteclip['duration']
                    amped_offset = 0
                    if 'cut' in cvpj_noteclip:
                        cutdata = cvpj_noteclip['cut']
                        cuttype = cutdata['type']
                        if cuttype == 'cut': 
                            amped_offset = cutdata['start']/4 if 'start' in cutdata else 0
                    amped_region = amped_makeregion(amped_position, amped_duration, amped_offset*4)

                    amped_notes = []

                    if 'notelist' in cvpj_noteclip:
                        for cvpj_note in cvpj_noteclip['notelist']:
                            if 0 <= cvpj_note['key']+60 <= 128:
                                amped_notes.append({
                                    "position": cvpj_note['position']/4, 
                                    "length": cvpj_note['duration']/4, 
                                    "key": int(cvpj_note['key']+60),
                                    "velocity": cvpj_note['vol']*100 if 'vol' in cvpj_note else 100, 
                                    "channel": 0
                                    })

                    amped_region["midi"]['notes'] = amped_notes

                    amped_trackdata["regions"].append(amped_region)

            if 'audio' in track_placements:
                cvpj_audioclips = notelist_data.sort(track_placements['audio'])
                for cvpj_audioclip in cvpj_audioclips:
                    amped_position = cvpj_audioclip['position']
                    amped_duration = cvpj_audioclip['duration']
                    amped_offset = 0

                    rate = 1

                    if 'cut' in cvpj_audioclip:
                        cutdata = cvpj_audioclip['cut']
                        cuttype = cutdata['type']
                        if cuttype == 'cut': 
                            amped_offset = cutdata['start']/4 if 'start' in cutdata else 0

                    if 'audiomod' in cvpj_audioclip:
                        cvpj_audiomod = cvpj_audioclip['audiomod']
                        stretch_method = cvpj_audiomod['stretch_method'] if 'stretch_method' in cvpj_audiomod else None
                        stretch_data = cvpj_audiomod['stretch_data'] if 'stretch_data' in cvpj_audiomod else {'rate': 1.0}
                        stretch_rate = stretch_data['rate'] if 'rate' in stretch_data else 1
                        if stretch_method == 'rate_speed': rate = stretch_rate
                        if stretch_method == 'rate_ignoretempo': rate = stretch_rate
                        if stretch_method == 'rate_tempo': rate = stretch_rate*(amped_bpm/120)

                    audioid = None
                    if 'file' in cvpj_audioclip:
                        audioid = addsample(zip_amped, cvpj_audioclip['file'])
                    amped_audclip = {}
                    amped_audclip['contentGuid'] = {}
                    if audioid != None: amped_audclip['contentGuid']['userAudio'] = {"exportedId": audioid}
                    amped_audclip['position'] = 0
                    amped_audclip['gain'] = cvpj_audioclip['vol'] if 'vol' in cvpj_audioclip else 1
                    amped_audclip['length'] = amped_duration+amped_offset
                    amped_audclip['offset'] = amped_offset
                    amped_audclip['stretch'] = 1/rate
                    amped_audclip['reversed'] = False

                    fadeinval = data_values.nested_dict_get_value(cvpj_audioclip, ['fade', 'in', 'duration'])
                    amped_audclip["fadeIn"] = fadeinval if fadeinval != None else 0

                    amped_region = amped_makeregion(amped_position, amped_duration, 0)
                    amped_region["clips"] = [amped_audclip]
                    amped_trackdata["regions"].append(amped_region)

                for autoname in [['vol','volume'], ['pan','pan']]:
                    autopoints = auto_nopl.getpoints(cvpj_l, ['track',cvpj_trackid,autoname[0]])
                    if autopoints != None: 
                        ampedauto = cvpjauto_to_ampedauto(auto.remove_instant(autopoints, 0, False))
                        amped_trackdata["automations"].append({"param": autoname[1], "points": ampedauto})

            if 'chain_fx_audio' in cvpj_trackdata:
                amped_effects = amped_parse_effects(cvpj_trackdata['chain_fx_audio'])
                for amped_effect in amped_effects:
                    amped_trackdata["devices"].append(amped_effect)

            amped_tracks.append(amped_trackdata)

        for aid in audio_id:
            amped_filenames[audio_id[aid]] = aid

        amped_out = {}
        amped_out["fileFormat"] = "AMPED SONG v1.3"
        amped_out["createdWith"] = "nothing"
        amped_out["settings"] = {"deviceDelayCompensation": True}
        amped_out["tracks"] = amped_tracks
        amped_out["masterTrack"] = {}
        amped_out["masterTrack"]['volume'] = 1
        amped_out["masterTrack"]['devices'] = []

        master_volume = 1
        if 'track_master' in cvpj_l: 
            cvpj_master = cvpj_l['track_master']
            amped_out["masterTrack"]['volume'] = data_values.get_value(cvpj_master, 'vol', 1.0)
            if 'chain_fx_audio' in cvpj_master:
                amped_out["masterTrack"]['devices'] = amped_parse_effects(cvpj_master['chain_fx_audio'])

        amped_out["workspace"] = {"library":False,"libraryWidth":300,"trackPanelWidth":160,"trackHeight":80,"beatWidth":24,"contentEditor":{"active":False,"trackId":5,"mode":"noteEditor","beatWidth":48,"noteEditorKeyHeight":10,"velocityPanelHeight":90,"velocityPanel":False,"audioEditorVerticalZoom":1,"height":400,"scroll":{"left":0,"top":0},"quantizationValue":0.25,"chordCreator":{"active":False,"scale":{"key":"C","mode":"Major"}}},"trackInspector":True,"trackInspectorTrackId":5,"arrangementScroll":{"left":0,"top":0},"activeTool":"arrow","timeDisplayInBeats":False,"openedDeviceIds":[],"virtualKeyboard":{"active":False,"height":187,"keyWidth":30,"octave":5,"scrollPositions":{"left":0,"top":0}},"xybeatz":{"active":False,"height":350,"zones":[{"genre":"Caribbean","beat":{"bpm":100,"name":"Zouk Electro 2"}},{"genre":"Soul Funk","beat":{"bpm":120,"name":"Defunkt"}},{"genre":"Greatest Breaks","beat":{"bpm":100,"name":"Walk This Way"}},{"genre":"Brazil","beat":{"bpm":95,"name":"Samba Partido Alto 1"}}],"parts":[{"x":0.75,"y":0.75,"gain":1},{"x":0.9,"y":0.2,"gain":1},{"x":0.8,"y":0.45,"gain":1},{"x":0.7,"y":0.7,"gain":1},{"x":0.7,"y":1,"gain":1},{"x":0.5,"y":0.5,"gain":1}],"partId":5,"fullKit":True,"soloPartId":-1,"complexity":50,"zoneId":0,"lastPartId":1},"displayedAutomations":{}}
        
        loop_on, loop_start, loop_end = song.get_loopdata(cvpj_l, 'r')
        amped_out["looping"] = {"active": loop_on, "start": loop_start/4, "end": loop_end/4}
        amped_out["tempo"] = amped_bpm
        amped_out["timeSignature"] = {"num": amped_numerator, "den": amped_denominator}
        amped_out["metronome"] = {"active": False, "level": 1}
        amped_out["playheadPosition"] = 0

        if 'timemarkers' in cvpj_l:
            for timemarkdata in cvpj_l['timemarkers']:
                if 'type' in timemarkdata:
                    if timemarkdata['type'] == 'loop_area':
                        amped_out["looping"] = {"active": True, "start": timemarkdata['position']/4, "end": timemarkdata['end']/4}

        zip_amped.writestr('amped-studio-project.json', json.dumps(amped_out))
        zip_amped.writestr('filenames.json', json.dumps(amped_filenames))
        zip_amped.close()
        open(output_file, 'wb').write(zip_bio.getbuffer())