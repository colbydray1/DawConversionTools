# SPDX-FileCopyrightText: 2023 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET
import pathlib

from functions import audio_wav
from functions import plugin_vst2
from functions import xtramath

from functions_plugparams import params_various_inst
from functions_plugparams import data_nullbytegroup

def convert_inst(instdata, platform_id):
	if platform_id == 'win':
		sampler_file_data = instdata['plugindata']
		wireturn = audio_wav.complete_wav_info(sampler_file_data)
		vst2_dll_vstpaths = plugin_vst2.vstpaths()
		if 'Grace' in vst2_dll_vstpaths['dll']:
			if 'file' in sampler_file_data and wireturn != None and wireturn == 1:
				file_extension = pathlib.Path(sampler_file_data['file']).suffix
				if file_extension == '.wav':
					gx_root = params_various_inst.grace_create_main()
					regionparams = {}
					regionparams['file'] = sampler_file_data['file']
					regionparams['length'] = sampler_file_data['length']
					regionparams['start'] = 0
					if 'loop' in sampler_file_data:
						regionparams['loop'] = sampler_file_data['loop']
					regionparams['end'] = sampler_file_data['length']
					params_various_inst.grace_create_region(gx_root, regionparams)
					xmlout = ET.tostring(gx_root, encoding='utf-8')
					plugin_vst2.replace_data(instdata, 'any', 'Grace', 'chunk', xmlout, None)
			else:
				print("[plug-conv] Unchanged, Grace (VST2) only supports Format 1 .WAV")
		else:
			print('[plug-conv] Unchanged, Plugin Grace not Found')

	# -------------------- sampler > vst2 (drops) --------------------

	if platform_id == 'lin':
		sampler_file_data = instdata['plugindata']
		wireturn = audio_wav.complete_wav_info(sampler_file_data)
		params_various_inst.drops_init()
		if 'file' in sampler_file_data: params_various_inst.drops_setfile(sampler_file_data['file'])

		if 'filter' in sampler_file_data: 
			if 'wet' in sampler_file_data['filter']: 
				if sampler_file_data['filter']['wet'] != 0:
					filterdata = sampler_file_data['filter']
					if 'cutoff' in filterdata: params_various_inst.drops_setvalue('cutoff', xtramath.clamp((filterdata['cutoff']/12000), 0, 1))
					if 'reso' in filterdata: params_various_inst.drops_setvalue('resonance', xtramath.clamp((filterdata['reso']/10), 0, 1))
					if 'type' in filterdata: 
						cvpj_filtertype = filterdata['type']
						if cvpj_filtertype == 'lowpass': params_various_inst.drops_setvalue('filter_type', 0)
						if cvpj_filtertype == 'bandpass': params_various_inst.drops_setvalue('filter_type', 1)
						if cvpj_filtertype == 'highpass': params_various_inst.drops_setvalue('filter_type', 2)

		if 'asdrlfo' in sampler_file_data: 
			if 'volume' in sampler_file_data['asdrlfo']: 
				if 'envelope' in sampler_file_data['asdrlfo']['volume']: 
					asdr_env = sampler_file_data['asdrlfo']['volume']['envelope']
					amountmul = 1
					if 'amount' in asdr_env: amountmul = xtramath.clamp(asdr_env['amount'], 0, 1)
					if 'attack' in asdr_env: params_various_inst.drops_setvalue('amp_attack', xtramath.clamp((asdr_env['attack']/10)*amountmul, 0, 1))
					if 'decay' in asdr_env: params_various_inst.drops_setvalue('amp_decay', xtramath.clamp((asdr_env['decay']/10)*amountmul, 0, 1))
					params_various_inst.drops_setvalue('amp_sustain', xtramath.clamp(asdr_env['sustain'], 0, 1))
					if 'release' in asdr_env: params_various_inst.drops_setvalue('amp_release', xtramath.clamp((asdr_env['release']/10)*amountmul, 0, 1))

				if 'lfo' in sampler_file_data['asdrlfo']['volume']: 
					asdr_lfo = sampler_file_data['asdrlfo']['volume']['lfo']
					params_various_inst.drops_setvalue('amp_lfo_depth', xtramath.clamp(asdr_lfo['amount'], 0, 1))
					if 'speed' in asdr_lfo:
						if asdr_lfo['speed']['type'] == 'seconds' and asdr_lfo['speed']['time'] != 0:
							params_various_inst.drops_setvalue('amp_lfo_freq', xtramath.clamp(((1/asdr_lfo['speed']['time'])*0.05), 0, 1))
					if 'shape' in asdr_lfo: params_various_inst.drops_setvalue('amp_lfo_type', params_various_inst.drops_shape(asdr_lfo['shape']))
					if 'attack' in asdr_lfo: params_various_inst.drops_setvalue('amp_lfo_fade', xtramath.clamp(asdr_lfo['attack']/10, 0, 1))

			if 'cutoff' in sampler_file_data['asdrlfo']: 
				if 'envelope' in sampler_file_data['asdrlfo']['cutoff']: 
					asdr_env = sampler_file_data['asdrlfo']['cutoff']['envelope']
					if 'amount' in asdr_env: params_various_inst.drops_setvalue('filter_eg_depth', xtramath.clamp((asdr_env['amount']/7300), 0, 1))
					if 'attack' in asdr_env: params_various_inst.drops_setvalue('filter_attack', xtramath.clamp((asdr_env['attack']/10), 0, 1))
					if 'decay' in asdr_env: params_various_inst.drops_setvalue('filter_decay', xtramath.clamp((asdr_env['decay']/10), 0, 1))
					params_various_inst.drops_setvalue('filter_sustain', xtramath.clamp(asdr_env['sustain'], 0, 1))
					if 'release' in asdr_env: params_various_inst.drops_setvalue('filter_release', xtramath.clamp((asdr_env['release']/10)*amountmul, 0, 1))

				if 'lfo' in sampler_file_data['asdrlfo']['cutoff']: 
					asdr_lfo = sampler_file_data['asdrlfo']['cutoff']['lfo']
					params_various_inst.drops_setvalue('filter_lfo_depth', xtramath.clamp(asdr_lfo['amount']/7300, 0, 1))
					if 'speed' in asdr_lfo:
						if asdr_lfo['speed']['type'] == 'seconds' and asdr_lfo['speed']['time'] != 0:
							params_various_inst.drops_setvalue('filter_lfo_freq', xtramath.clamp(((1/asdr_lfo['speed']['time'])*0.05), 0, 1))
					if 'shape' in asdr_lfo: params_various_inst.drops_setvalue('filter_lfo_type', params_various_inst.drops_shape(asdr_lfo['shape']))
					if 'attack' in asdr_lfo: params_various_inst.drops_setvalue('filter_lfo_fade', xtramath.clamp(asdr_lfo['attack']/10, 0, 1))

		plugin_vst2.replace_data(vst_instdata, 'lin', 'Drops', 'chunk', data_nullbytegroup.make(params_various_inst.drops_get()), None)
