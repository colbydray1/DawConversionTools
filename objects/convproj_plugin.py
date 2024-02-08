# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from functions import xtramath
from functions import data_values
import base64

from objects import convproj_placements
from objects_convproj import params
from objects_convproj import visual
from objects_convproj import autopoints
from objects_convproj import envelope
from objects_convproj import wave
from objects_convproj import harmonics

def vis_plugin(p_type, p_subtype):
    if p_type != None and p_subtype != None: return p_type+':'+p_subtype
    elif p_type != None and p_subtype == None: return p_type
    elif p_type == None and p_subtype == None: return 'None'

class cvpj_filter:
    def __init__(self):
        self.on = False
        self.type = None
        self.subtype = None
        self.freq = 44100
        self.q = 1
        self.gain = 0
        self.slope = 12
        self.filter_algo = ''

class cvpj_lfo:
    def __init__(self):
        self.predelay = 0
        self.attack = 0
        self.shape = 'sine'
        self.speed_type = 'seconds'
        self.speed_time = 1
        self.amount = 0

class cvpj_wavetable:
    def __init__(self):
        self.ids = ids
        self.locs = locs
        self.phase = phase

class cvpj_regions:
    def __init__(self):
        self.data = []

    def add(self, i_min, i_max, i_data):
        self.data.append([i_min, i_max, i_data])

class cvpj_osc:
    def __init__(self):
        self.shape = 'square'
        self.name_id = ''
        self.params = {}
        self.env = {}

class cvpj_plugin:
    def __init__(self):
        self.cvpjdata = {}
        self.plugin_type = None
        self.plugin_subtype = None
        self.visual = visual.cvpj_visual()
        self.params = params.cvpj_paramset()
        self.params_slot = params.cvpj_paramset()
        self.datavals = params.cvpj_datavals()
        self.bytesdata = {}
        self.regions = cvpj_regions()
        self.env_adsr = {}
        self.env_points = {}
        self.env_points_vars = {}
        self.env_blocks = {}
        self.filter = cvpj_filter()
        self.eq = []
        self.named_eq = {}
        self.lfos = {}
        self.waves = {}
        self.harmonics = {}
        self.wavetables = {}
        self.filerefs = {}
        self.samplerefs = {}
        self.oscs = []

    def type_set(self, i_type, i_subtype):
        self.plugin_type = i_type
        self.plugin_subtype = i_subtype

    def type_get(self):
        return [self.plugin_type, self.plugin_subtype]

    def get_type_visual(self):
        return vis_plugin(self.plugin_type, self.plugin_subtype)

    def replace(self, i_type, i_subtype):
        self.plugin_type = i_type
        self.plugin_subtype = i_subtype
        self.params.clear()
        self.data = {}

    def check_match(self, i_type, i_subtype):
        return self.plugin_type==i_type and self.plugin_subtype==i_subtype

    def check_matchmulti(self, i_type, i_subtypes):
        return self.plugin_type==i_type and (self.plugin_subtype in i_subtypes)

    def check_wildmatch(self, i_type, i_subtype):
        if self.plugin_type==i_type:
            if self.plugin_subtype==i_subtype: return True
            elif i_subtype == None: return True
            else: return False
        else: return False

    # -------------------------------------------------- fxdata
    def fxdata_add(self, i_enabled, i_wet):
        if i_enabled != None: self.params_slot.add('enabled', i_enabled, 'bool')
        if i_wet != None: self.params_slot.add('wet', i_wet, 'float')

    def fxdata_get(self):
        i_enabled = self.params_slot.get('enabled', 1).value
        i_wet = self.params_slot.get('wet', 1).value
        return i_enabled, i_wet

    # -------------------------------------------------- param
    def add_from_dset(self, p_id, p_value, dset, ds_cat, ds_group): 
        defparams = dset.params_i_get(ds_cat, ds_group, p_id)
        if defparams != None:
            if p_value == None: p_value = defparams[2]
            if defparams[0] == False:
                param_obj = self.params.add(p_id, p_value, defparams[1])
                param_obj.min = defparams[3]
                param_obj.max = defparams[4]
                param_obj.visual.name = defparams[5]
            else:
                self.datavals.add(p_id, p_value)
        else:
            if p_value == None: p_value = 0
            self.params.add(p_id, p_value, 'float')

    def param_dict_dataset_get(self, i_dict, dataset, catname, pluginname):
        paramlist = dataset.params_list(catname, pluginname)
        if paramlist:
            for param in paramlist:
                outval = data_values.nested_dict_get_value(i_dict, param.split('/'))
                self.add_from_dset(param, outval, dataset, catname, pluginname)

    def param_dict_dataset_set(self, dataset, catname, pluginname):
        paramlist = dataset.params_list(catname, pluginname)
        outdict = {}
        if paramlist:
            for param in paramlist:
                defparams = dataset.params_i_get(catname, pluginname, param)
                if not defparams[0]: outdata = self.params.get(param, defparams[2]).value
                else: outdata = self.datavals.get(param, defparams[2])
                data_values.nested_dict_add_value(outdict, param.split('/'), outdata)
        return outdict

    # -------------------------------------------------- rawdata
    def rawdata_add(self, i_name, i_databytes):
        self.bytesdata[i_name] = i_databytes

    def rawdata_add_b64(self, i_name, i_databytes):
        self.bytesdata[i_name] = base64.b64decode(i_databytes)

    def rawdata_get(self, i_name):
        return self.bytesdata[i_name] if i_name in self.bytesdata else b''

    def rawdata_get_b64(self, i_name):
        return base64.b64encode(self.bytesdata[i_name] if i_name in self.bytesdata else b'').decode('ascii')

    # -------------------------------------------------- regions
    def region_add(self, i_name, i_min, i_max, i_value):
        if i_name not in self.regions: self.regions[i_name] = cvpj_regions()
        self.regions[i_name].add(i_min, i_max, i_value)

    def regions_get(self, i_name):
        return self.regions[i_name] if i_name in self.regions else cvpj_regions()

    # -------------------------------------------------- asdr_env
    def env_asdr_add(self, a_type, a_predelay, a_attack, a_hold, a_decay, a_sustain, a_release, a_amount):
        adsr_obj = envelope.cvpj_envelope_adsr()
        adsr_obj.predelay = a_predelay
        adsr_obj.attack = a_attack
        adsr_obj.hold = a_hold
        adsr_obj.decay = a_decay
        adsr_obj.sustain = a_sustain
        adsr_obj.release = a_release
        adsr_obj.amount = a_amount
        if a_type not in self.env_adsr: self.env_adsr[a_type] = {}
        self.env_adsr[a_type] = adsr_obj
        return adsr_obj

    def env_asdr_tension_add(self, a_type, t_attack, t_decay, t_release):
        if a_type in self.env_adsr: 
            self.env_adsr[a_type].attack_tension = t_attack
            self.env_adsr[a_type].decay_tension = t_decay
            self.env_adsr[a_type].release_tension = t_release

    def env_asdr_get(self, a_type):
        if a_type in self.env_adsr: return self.env_adsr[a_type]
        return envelope.cvpj_envelope_adsr()

    def env_asdr_get_exists(self, a_type): 
        if a_type in self.env_adsr: return True, self.env_adsr[a_type]
        return False, envelope.cvpj_envelope_adsr()

    def env_asdr_list(self): 
        return [x for x in self.env_adsr]

    # -------------------------------------------------- env_blocks
    def env_blocks_add(self, a_type, a_vals, a_time, a_max, a_loop, a_release):
        blocks_obj = envelope.cvpj_envelope_blocks()
        blocks_obj.values = a_vals
        blocks_obj.time = a_time
        blocks_obj.max = a_max
        blocks_obj.loop = a_loop
        blocks_obj.release = a_release
        if a_type not in self.env_blocks: self.env_blocks[a_type] = {}
        self.env_blocks[a_type] = blocks_obj

    def env_blocks_get(self, a_type): 
        if a_type in self.env_blocks: return self.env_blocks[a_type]
        return envelope.cvpj_envelope_blocks()

    def env_blocks_get_exists(self, a_type): 
        if a_type in self.env_blocks: return True, self.env_blocks[a_type]
        return False, envelope.cvpj_envelope_blocks()

    def env_blocks_list(self): 
        return [x for x in self.env_blocks]

    # -------------------------------------------------- env_points
    def env_points_add(self, a_type, time_ppq, time_float, val_type):
        self.env_points[a_type] = autopoints.cvpj_autopoints(time_ppq, time_float, val_type)
        return self.env_points[a_type]

    def env_points_get(self, a_type): 
        if a_type in self.env_points: return self.env_points[a_type]
        return autopoints.cvpj_autopoints(1, True, 'float')

    def env_points_get_exists(self, a_type): 
        if a_type in self.env_points: return True, self.env_points[a_type]
        return False, autopoints.cvpj_autopoints(1, True, 'float')

    def env_points_addvar(self, a_type, p_name, p_value):
        if a_type in self.env_points_vars: self.env_points_vars[a_type] = {}
        self.env_points_vars[a_type][p_name] = p_value

    def env_points_from_blocks(self, a_type):
        blocks_obj = self.env_blocks_get(a_type)
        points_obj = self.env_points_add(a_type, 4, True, 'float')
        for numblock in range(len(blocks_obj.values)): 
            apoint_obj = points_obj.add_point()
            apoint_obj.pos = numblock*blocks_obj.time
            apoint_obj.value = xtramath.between_to_one(0, blocks_obj.max, blocks_obj.values[numblock])

    def env_asdr_from_points(self, a_type):
        env_pointsdata = self.env_points_get(a_type)
        env_pointsdata.change_timings(1, True)

        sustainpoint = env_pointsdata.data['sustain'] if 'sustain' in env_pointsdata.data else None
        fadeout = env_pointsdata.data['fadeout'] if 'fadeout' in env_pointsdata.data else 0
        pointsdata = env_pointsdata.points
        numpoints = len(pointsdata)

        adsr_obj = self.env_asdr_add(a_type, 0, 0, 0, 0, 1, 0, 1)

        sustainnum = None if (sustainpoint == None or sustainpoint == numpoints) else sustainpoint
        isenvconverted = 0

        #print('numpoints', numpoints)
        if numpoints == 2:
            env_duration = pointsdata[1].pos
            env_value = pointsdata[0].value - pointsdata[1].value
            maxval = max(pointsdata[0].value, pointsdata[1].value)
            minval = min(pointsdata[0].value, pointsdata[1].value)
    
            if pointsdata[0].value != pointsdata[1].value:
                if sustainnum == None:
                    if env_value > 0:
                        adsr_obj.decay = env_duration
                        adsr_obj.sustain = 0
                        if a_type == 'vol': adsr_obj.amount = 1-minval
                        print("[env_asdr_from_points] 2 | ^_")
                        isenvconverted = 201 #debug
                    else: 
                        adsr_obj.attack = env_duration
                        adsr_obj.release = fadeout
                        print("[env_asdr_from_points] 2 | _^")
                        isenvconverted = 202 #debug
    
                elif sustainnum == 1:
                    if env_value >= 0: 
                        adsr_obj.release = env_duration
                        isenvconverted = 203 #debug
                    else:
                        adsr_obj.release = env_duration
                        adsr_obj.amount = -1
                        isenvconverted = 204 #debug
    
        elif numpoints == 3:
            envp_middle = pointsdata[1].pos
            envp_end = pointsdata[2].pos
            envv_first = pointsdata[0].value
            envv_middle = pointsdata[1].value
            envv_end = pointsdata[2].value
            firstmid_s = envv_first-envv_middle
            midend_s = envv_end-envv_middle
            #print(envp_middle, envp_end, '|', envv_first, envv_middle, envv_end)
            if firstmid_s > 0 and sustainnum == None: a_sustain = 0

            if firstmid_s > 0 and midend_s == 0:
                print("[env_asdr_from_points] 3 | ^__" )
                if sustainnum == None: adsr_obj.decay = envp_middle
                if sustainnum == 1: adsr_obj.release = envp_middle
                isenvconverted = 300

            elif firstmid_s > 0 and midend_s < 0:
                print("[env_asdr_from_points] 3 | ^._" )
                if sustainnum == None: 
                    adsr_obj.decay = envp_end
                    adsr_obj.decay_tension = (envv_middle-(envv_first/2))*2
                    isenvconverted = 301
    
                if sustainnum == 1: 
                    adsr_obj.release = envp_end
                    adsr_obj.release_tension = ((((envp_middle/envp_end)/2)+(envv_middle/2))-0.5)*2
                    isenvconverted = 302
    
                if sustainnum == 2: 
                    adsr_obj.decay = envp_middle
                    adsr_obj.release = envp_end-envp_middle
                    adsr_obj.sustain = envv_middle
                    isenvconverted = 303
    

            elif firstmid_s < 0 and midend_s < 0:
                print("[env_asdr_from_points] 3 | _^." )
                if sustainnum in [None, 1]: 
                    adsr_obj.attack = envp_middle
                    adsr_obj.decay = (envp_end-envp_middle)
                    adsr_obj.sustain = envv_end
                    isenvconverted = 304
                if sustainnum == 2: 
                    adsr_obj.attack = envp_middle
                    adsr_obj.release = (envp_end-envp_middle)
                    isenvconverted = 305

            elif firstmid_s == 0 and midend_s < 0:
                print("[env_asdr_from_points] 3 | ^^.")
                if sustainnum in [None, 1]:
                    adsr_obj.hold = envp_middle
                    adsr_obj.decay = envp_end-envp_middle
                    adsr_obj.sustain = envv_end
                    isenvconverted = 306
                if sustainnum == 2: 
                    adsr_obj.hold = envp_middle
                    adsr_obj.release = envp_end-envp_middle
                    isenvconverted = 307
    
            elif firstmid_s < 0 and midend_s > 0:
                print("[env_asdr_from_points] 3 | _.^")
                adsr_obj.attack = envp_end
                adsr_obj.attack_tension = ((envp_end-envp_middle)-1)
                isenvconverted = 308
    
            elif firstmid_s == 0 and midend_s > 0:
                print("[env_asdr_from_points] 3 | __^")
                adsr_obj.predelay = envp_middle
                adsr_obj.attack = envp_end-envp_middle
                isenvconverted = 309

            elif firstmid_s < 0 and midend_s == 0:
                print("[env_asdr_from_points] 3 | _^^")
                adsr_obj.attack = envp_middle
                adsr_obj.hold = envp_end-envp_middle
                isenvconverted = 310

            #elif firstmid_s > 0 and midend_s > 0:
            #    print("[env_asdr_from_points] 3 | ^.^")
            #    if sustainnum in [None, 1]:
            #        adsr_obj.attack = envp_middle
            #        a_decay = (envp_end-envp_middle)
            #        a_amount = envv_middle-1
            #    if sustainnum == 2: 
            #        adsr_obj.attack = envp_middle
            #        adsr_obj.release = (envp_end-envp_middle)
            #        a_amount = envv_middle-1
            #    isenvconverted = True
    
            if isenvconverted != 0 and adsr_obj.sustain != 0 and adsr_obj.release == 0: adsr_obj.release = fadeout

    def env_points_list(self): 
        return [x for x in self.env_points]

    # -------------------------------------------------- lfo
    def lfo_add(self, a_type): 
        lfo_obj = cvpj_lfo()
        self.lfos[a_type] = lfo_obj
        return lfo_obj

    def lfo_get(self, a_type): return self.lfos[a_type] if a_type in self.lfos else cvpj_lfo()
    def lfo_list(self): return [x for x in self.lfos]

    # -------------------------------------------------- osc
    def osc_add(self): 
        osc_obj = cvpj_osc()
        self.oscs.append(osc_obj)
        return osc_obj

    # -------------------------------------------------- wave
    def wave_add(self, i_name): 
        self.waves[i_name] = wave.cvpj_wave()
        return self.waves[i_name]
    def wave_get(self, i_name): return self.waves[i_name] if i_name in self.waves else wave.cvpj_wave()
    def wave_list(self):  return [x for x in self.waves]

    # -------------------------------------------------- harmonics
    def harmonics_add(self, i_name): 
        self.harmonics[i_name] = harmonics.cvpj_harmonics()
        return self.harmonics[i_name]
    def harmonics_get(self, i_name): return self.harmonics[i_name] if i_name in self.harmonics else harmonics.cvpj_harmonics()
    def harmonics_list(self): return [x for x in self.harmonics]

    # -------------------------------------------------- wave
    def wavetable_add(self, i_name, i_wavenames, i_wavelocs, i_phase): 
        self.wavetable[i_name] = cvpj_wavetable()
        self.wavetable[i_name].ids = i_wavenames
        self.wavetable[i_name].locs = i_wavelocs
        self.wavetable[i_name].phase = i_phase
    def wavetable_get(self, i_name): return self.wavetables[i_name] if i_name in self.wavetables else cvpj_wavetable()
    def wavetable_list(self):  return [x for x in self.wavetables]

    # -------------------------------------------------- sampler
    def sampler_calc_pos(self, sampleref_obj, sample_start, sample_loop): 
        point_value_type = self.datavals.get('point_value_type', 'samples')

        out_start = 0
        out_loop = 0
        out_end = 1

        loopenabled = 0
        loopmode = "normal"

        if point_value_type == 'samples' and sampleref_obj.dur_samples:
            if sampleref_obj.dur_samples != 0:
                out_start = sample_start/sampleref_obj.dur_samples

                if sample_loop:
                    if 'points' in sample_loop:
                        sample_loop_points = sample_loop['points']
                        out_loop = sample_loop_points[0] / sampleref_obj.dur_samples
                        out_end = sample_loop_points[1] / sampleref_obj.dur_samples
                        if out_end == 0 or out_start == out_end: out_end = 1.0

        if point_value_type == 'percent':
            out_start = sample_start
            if sample_loop:
                if 'points' in sample_loop:
                    trkJ_loop_points = sample_loop['points']
                    out_loop = trkJ_loop_points[0]
                    out_end = trkJ_loop_points[1]

        return out_start, out_loop, out_end

    # -------------------------------------------------- sampleref

    def sampleref_fileref(self, sampleref_name, convproj_obj): 
        if sampleref_name in self.samplerefs:
            sampleref_id = self.samplerefs[sampleref_name]
            return convproj_obj.get_sampleref(sampleref_id)
        return False, None

    def getpath_sampleref(self, sampleref_name, convproj_obj, os_type, relative): 
        outpath = ''
        if sampleref_name in self.samplerefs:
            ref_found, sampleref_obj = convproj_obj.get_sampleref(self.samplerefs[sampleref_name])
            if ref_found: outpath = sampleref_obj.fileref.get_path(os_type, relative)
        return outpath

    # -------------------------------------------------- fileref

    def get_fileref(self, fileref_name, convproj_obj): 
        if fileref_name in self.filerefs:
            fileref_id = self.filerefs[fileref_name]
            return convproj_obj.get_fileref(fileref_id)
        return False, None

    def getpath_fileref(self, convproj_obj, refname, os_type, relative): 
        ref_found, fileref_obj = self.get_fileref(refname, convproj_obj)
        return fileref_obj.get_path(os_type, relative) if ref_found else ''

    # -------------------------------------------------- eq
    def eq_add(self): 
        filter_obj = cvpj_filter()
        self.eq.append(filter_obj)
        return filter_obj

    # -------------------------------------------------- named_eq
    def named_eq_add(self, eq_name): 
        if eq_name not in self.named_eq: self.named_eq[eq_name] = []
        filter_obj = cvpj_filter()
        self.named_eq[eq_name].append(filter_obj)
        return filter_obj
