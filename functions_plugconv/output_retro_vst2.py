# SPDX-FileCopyrightText: 2023 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET
import pathlib

from functions import audio_wav
from functions import plugin_vst2
from functions import vst_inst

from functions_plugparams import data_vc2xml

def convert_inst(instdata, out_daw):
	pluginname = instdata['plugin']
	plugindata = instdata['plugindata']

	if pluginname == 'retro':
		vst_inst.m8bp_init()
		if 'attack' in plugindata: vst_inst.m8bp_setvalue("attack", plugindata['attack'])
		if 'decay' in plugindata: vst_inst.m8bp_setvalue("decay", plugindata['decay'])
		if 'sustain' in plugindata: vst_inst.m8bp_addvalue("suslevel", plugindata['sustain'])
		if 'release' in plugindata: vst_inst.m8bp_setvalue("release", plugindata['release'])

		if 'duty' in plugindata: 
			if plugindata['duty'] == 0: vst_inst.m8bp_setvalue("duty", 2)
			if plugindata['duty'] == 1: vst_inst.m8bp_setvalue("duty", 1)
			if plugindata['duty'] == 2: vst_inst.m8bp_setvalue("duty", 0)
		if 'type' in plugindata:
			if plugindata['type'] == '1bit_short': vst_inst.m8bp_setvalue("duty", 0)
			if plugindata['type'] == '4bit': vst_inst.m8bp_setvalue("duty", 1)

		if 'env_arp' in plugindata:
			vst_inst.m8bp_setvalue("isPitchSequenceEnabled_raw", 1.0)
			vst_inst.m8bp_setenv('pitch', plugindata['env_arp']['values'])

		if 'env_duty' in plugindata:
			vst_inst.m8bp_setvalue("isDutySequenceEnabled_raw", 1.0)
			vst_inst.m8bp_setenv('duty', plugindata['env_duty']['values'])

		if 'env_vol' in plugindata:
			vst_inst.m8bp_setvalue("isVolumeSequenceEnabled_raw", 1.0)
			vst_inst.m8bp_setenv('volume', plugindata['env_vol']['values'])

		if plugindata['wave'] == 'square': vst_inst.m8bp_setvalue("osc", 0.0)
		if plugindata['wave'] == 'triangle': vst_inst.m8bp_setvalue("osc", 1.0)
		if plugindata['wave'] == 'noise': vst_inst.m8bp_setvalue("osc", 2.0)

		plugin_vst2.replace_data(instdata, 'any', 'Magical 8bit Plug 2', 'chunk', data_vc2xml.make(vst_inst.m8bp_out()), None)
