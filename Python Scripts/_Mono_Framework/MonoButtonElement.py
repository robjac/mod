# by amounra 0413 : http://www.aumhaa.com

import Live
from _Framework.ButtonElement import ButtonElement, ON_VALUE, OFF_VALUE
from _Framework.InputControlElement import InputControlElement
from _Framework.NotifyingControlElement import NotifyingControlElement
from _Framework.Skin import Skin, SkinColorMissingError
from LividColors import *

from Debug import *

MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE,
 MIDI_CC_TYPE,
 MIDI_PB_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224

debug = initialize_debug()

class MonoButtonElement(ButtonElement):
	__module__ = __name__
	__doc__ = ' Special button class that can be configured with custom on- and off-values, some of which flash at specified intervals called by _Update_Display'


	def __init__(self, is_momentary, msg_type, channel, identifier, name, cs, *a, **k):
		super(MonoButtonElement, self).__init__(is_momentary, msg_type, channel, identifier, *a, **k)
		self.name = name
		self._script = cs
		self._color_map = [2, 64, 4, 8, 16, 127, 32]
		self._num_colors = 7
		self._num_flash_states = 18
		self._flash_state = 0
		self._color = 0
		self._on_value = 127
		self._off_value = 0
		self._darkened = 0
		self._is_enabled = True
		self._force_forwarding = False
		self._is_notifying = False
		self._force_next_value = False
		self._parameter = None
		self._report_input = True
	

	def set_color_map(self, color_map):
		assert isinstance(color_map, tuple)
		assert len(color_map) > 0
		self._num_colors = len(color_map)
		self._num_flash_states = int(127/len(color_map))
		self._color_map = color_map
	

	def set_on_off_values(self, on_value, off_value):
		self._last_sent_message = None
		self._on_value = on_value
		self._off_value = off_value
	

	def set_on_value(self, value):
		self._last_sent_message = None
		self._on_value = value
	

	def set_off_value(self, value):
		self._last_sent_message = None
		self._off_value = value
	

	def set_force_next_value(self):
		self._last_sent_message = None
		self._force_next_value = True

	def set_enabled(self, enabled):
		self._is_enabled = enabled
		self._request_rebuild()

	def turn_on(self, force = False):
		self.force_next_send()
		if self._on_value in range(0, 128):
			self.send_value(self._on_value)
		else:
			try:
				color = self._skin[self._on_value]
				color.draw(self)
			except SkinColorMissingError:
				#super(MonoButtonElement, self).turn_on()
				debug('skin color missing', self._on_value)
				self.send_value(127)
	

	def turn_off(self, force = False):
		self.force_next_send()
		if self._off_value in range(0, 128):
			self.send_value(self._off_value)
		else:
			try:
				color = self._skin[self._off_value]
				color.draw(self)
			except SkinColorMissingError:
				#super(MonoButtonElement, self).turn_off()
				debug('skin color missing', self._off_value)
				self.send_value(0)
	

	def reset(self, force = False):
		self.force_next_send()
		self.send_value(0)
	

	def receive_value(self, value):
		self._last_sent_message = None
		ButtonElement.receive_value(self, value)
	

	def set_light(self, value, *a, **k):
		try:
			self._skin[value]
		except SkinColorMissingError:
			debug('skin missing for', value)
		super(MonoButtonElement, self).set_light(value, *a, **k)
	

	def send_value(self, value, force = False):
		if (value != None) and isinstance(value, int) and (value in range(128)):
			if (force or self._force_next_send or ((value != self._last_sent_value) and self._is_being_forwarded)):
				data_byte1 = self._original_identifier
				if value in range(1, 127):
					data_byte2 = self._color_map[(value - 1) % (self._num_colors)]
				elif value == 127:
					data_byte2 = self._color_map[self._num_colors-1]
				else:
					data_byte2 = self._darkened
				self._color = data_byte2
				status_byte = self._original_channel
				if (self._msg_type == MIDI_NOTE_TYPE):
					status_byte += MIDI_NOTE_ON_STATUS
				elif (self._msg_type == MIDI_CC_TYPE):
					status_byte += MIDI_CC_STATUS
				else:
					assert False
				self.send_midi(tuple([status_byte,
				 data_byte1,
				 data_byte2]))
				self._last_sent_message = [value]
				if self._report_output:
					is_input = True
					self._report_value(value, (not is_input))
				self._flash_state = round((value -1)/self._num_colors)
				self._force_next_value = False
		else:
			debug('Button bad send value:', value)
	

	def script_wants_forwarding(self):
		if not self._is_enabled and not self._force_forwarding:
			return False
		else:
			return InputControlElement.script_wants_forwarding(self)
	

	def flash(self, timer):
		if (self._is_being_forwarded and self._flash_state in range(1, self._num_flash_states) and (timer % self._flash_state) == 0):
			data_byte1 = self._original_identifier
			data_byte2 = self._color * int((timer % (self._flash_state * 2)) > 0)
			status_byte = self._original_channel
			if (self._msg_type == MIDI_NOTE_TYPE):
				status_byte += MIDI_NOTE_ON_STATUS
			elif (self._msg_type == MIDI_CC_TYPE):
				status_byte += MIDI_CC_STATUS
			else:
				assert False
			self.send_midi((status_byte,
			 data_byte1,
			 data_byte2))
			
	

