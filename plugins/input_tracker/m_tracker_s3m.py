# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import io
import plugins
import os.path
from functions import data_bytes

TEXTSTART = 's3m_inst_'
MAINCOLOR = [0.65, 0.57, 0.33]

class input_s3m(plugins.base):
	def is_dawvert_plugin(self): 
		return 'input'

	def get_shortname(self): 
		return 's3m'

	def get_name(self): 
		return 'Scream Tracker 3 Module'

	def get_priority(self): 
		return 0

	def get_prop(self, in_dict): 
		in_dict['file_ext'] = ['s3m']
		in_dict['track_lanes'] = True
		in_dict['audio_filetypes'] = ['wav']
		in_dict['plugin_included'] = ['universal:sampler:single']
		in_dict['projtype'] = 'm'

	def get_detect_info(self, detectdef_obj):
		detectdef_obj.headers.append([44, b'SCRM'])

	def parse(self, convproj_obj, dawvert_intent):
		from objects.file_proj import tracker_s3m as proj_s3m
		from objects.tracker import pat_single
		
		project_obj = proj_s3m.s3m_song()
		if dawvert_intent.input_mode == 'file':
			if not project_obj.load_from_file(dawvert_intent.input_file): exit()
		if dawvert_intent.input_mode == 'bytes':
			if not project_obj.load_from_raw(dawvert_intent.input_data): exit()

		samplefolder = dawvert_intent.path_samples['extracted']
		
		current_tempo = project_obj.tempo
		current_speed = project_obj.speed

		tempo_slide = 0

		t_orderlist = project_obj.l_order.copy()[0:-1]
		while 255 in t_orderlist: t_orderlist.remove(255)
		
		# ------------- Instruments -------------
		for s3m_numinst, s3m_inst in enumerate(project_obj.instruments):
			cvpj_instid = TEXTSTART + str(s3m_numinst+1)

			if s3m_inst.filename != '': cvpj_inst_name = s3m_inst.filename
			elif s3m_inst.name != '': cvpj_inst_name = s3m_inst.name
			else: cvpj_inst_name = ' '

			wave_path = samplefolder+str(s3m_numinst).zfill(2)+'.wav'
			inst_obj = convproj_obj.instrument__add(cvpj_instid)
			inst_obj.visual.name = cvpj_inst_name
			inst_obj.visual.color.set_float([0.32, 0.27, 0.16] if not s3m_inst.type else [0.65, 0.57, 0.33])
			inst_obj.params.add('vol', 0.3, 'float')

			if s3m_inst.type == 1:
				s3m_inst.rip_sample(samplefolder, project_obj.samptype, wave_path)
				plugin_obj, pluginid, sampleref_obj, sp_obj = convproj_obj.plugin__addspec__sampler__genid(wave_path, None)
				sp_obj.point_value_type = "samples"

				if s3m_inst.sampleloc != 0 and s3m_inst.length != 0:
					sp_obj.loop_active = s3m_inst.loopon
					sp_obj.loop_start = s3m_inst.loopStart
					sp_obj.loop_end = s3m_inst.loopEnd

				inst_obj.plugslots.set_synth(pluginid)

		patterndata_obj = pat_single.single_patsong(32, TEXTSTART, MAINCOLOR)
		patterndata_obj.orders = t_orderlist

		for patnum, s3mpat_obj in enumerate(project_obj.patterns):
			pattern_obj = patterndata_obj.pattern_add(patnum, 64)
			for rownum, rowdatas in enumerate(s3mpat_obj.data):
				for c_channel, c_note, c_inst, c_vol, c_command, c_info in rowdatas:

					out_vol = None

					if c_note == 255: c_note = None

					if c_vol != None: out_vol = c_vol/64
					elif c_inst != None and c_inst-1 < len(project_obj.instruments): 
						out_vol = project_obj.instruments[c_inst-1].volume/64

					if out_vol != None: pattern_obj.cell_param(c_channel, rownum, 'vol', out_vol)

					if c_note != None:
						if c_inst != None:
							note_oct, note_tone = data_bytes.splitbyte(c_note)
							out_note = (note_oct-4)*12 + note_tone if c_note != 254 else 'cut'
						else:
							out_note = None
						pattern_obj.cell_note(c_channel, rownum, out_note, None if c_inst == 0 else c_inst)

					if c_command != None or c_info != None:
						pattern_obj.cell_fx_s3m(c_channel, rownum, c_command, c_info)

						if c_command == 20: 
							tempoval = c_info
							if c_info == 0: current_tempo += tempo_slide
							if 0 < c_info < 32:
								tempo_slide = c_info-16
								current_tempo += c_info-16
							if c_info > 32: current_tempo = c_info
							pattern_obj.cell_g_param(c_channel, rownum, 'tempo', current_tempo)

						if c_command == 26: 
							pattern_obj.cell_param(c_channel, rownum, 'pan', ((c_info/128)-0.5)*2)
						  
		patterndata_obj.to_cvpj(convproj_obj, TEXTSTART, project_obj.tempo, project_obj.speed, False, MAINCOLOR)

		convproj_obj.metadata.name = project_obj.name
		convproj_obj.metadata.comment_text = '\r'.join([i.name for i in project_obj.instruments])
		
		convproj_obj.do_actions.append('do_addloop')
		convproj_obj.do_actions.append('do_lanefit')
