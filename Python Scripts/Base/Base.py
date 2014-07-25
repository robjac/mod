# by amounra 0613 : http://www.aumhaa.com

from __future__ import with_statement
import Live
import math
import sys
from _Tools.re import *
from itertools import imap, chain, starmap

""" _Framework files """
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.ControlElement import ControlElement, ControlElementClient
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.DisplayDataSource import DisplayDataSource
from _Framework.DeviceComponent import DeviceComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import *
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.NotifyingControlElement import NotifyingControlElement
from _Framework.SceneComponent import SceneComponent
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent as SessionZoomingComponent
from _Framework.SliderElement import SliderElement
from _Framework.TransportComponent import TransportComponent
from _Framework.PhysicalDisplayElement import *
from _Framework.SubjectSlot import subject_slot, subject_slot_group
from _Framework.Layer import Layer
from _Framework.Skin import Skin
from _Framework.M4LInterfaceComponent import M4LInterfaceComponent
from _Framework.ComboElement import ComboElement, DoublePressElement, MultiElement, DoublePressContext
from _Framework.ModesComponent import Mode, CompoundMode, DisableMode, EnablingModesComponent, DelayMode, AddLayerMode, LayerMode, MultiEntryMode, ModesComponent, SetAttributeMode, ModeButtonBehaviour, CancellableBehaviour, AlternativeBehaviour, ReenterBehaviour, DynamicBehaviourMixin, ExcludingBehaviourMixin, ImmediateBehaviour, LatchingBehaviour, ModeButtonBehaviour
from _Framework.ClipCreator import ClipCreator
from _Framework.Resource import PrioritizedResource
from _Framework.Util import mixin

"""Custom files, overrides, and files from other scripts"""
from _Mono_Framework.MonoButtonElement import *
from _Mono_Framework.MonoEncoderElement import MonoEncoderElement
from _Mono_Framework.MonoBridgeElement import MonoBridgeElement
from _Mono_Framework.MonoDeviceComponent import MonoDeviceComponent
from _Mono_Framework.DeviceNavigator import DeviceNavigator
from _Mono_Framework.TranslationComponent import TranslationComponent
from _Mono_Framework.ModDevices import *
from _Mono_Framework.Mod import *
from _Mono_Framework.Debug import *

import _Mono_Framework.modRemixNet as RemixNet
import _Mono_Framework.modOSC


from Push.AutoArmComponent import AutoArmComponent
from Push.SessionRecordingComponent import *
from Push.ViewControlComponent import ViewControlComponent
from Push.DrumGroupComponent import DrumGroupComponent
from Push.StepSeqComponent import StepSeqComponent
from Push.PlayheadElement import PlayheadElement
from Push.PlayheadComponent import PlayheadComponent
from Push.GridResolution import GridResolution
from Push.ConfigurableButtonElement import ConfigurableButtonElement
from Push.LoopSelectorComponent import LoopSelectorComponent
from Push.Actions import CreateInstrumentTrackComponent, CreateDefaultTrackComponent, CaptureAndInsertSceneComponent, DuplicateDetailClipComponent, DuplicateLoopComponent, SelectComponent, DeleteComponent, DeleteSelectedClipComponent, DeleteSelectedSceneComponent, CreateDeviceComponent
from Push.SkinDefault import make_default_skin

from MonoScaleComponent import *

DIRS = [47, 48, 50, 49]
_NOTENAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
NOTENAMES = [(_NOTENAMES[index%12] + ' ' + str(int(index/12))) for index in range(128)]
from Map import *

MODE_DATA = {'Clips': 'L', 
			'Clips_shifted': 'L', 
			'Sends': 'S',
			'Sends_shifted': 'S',
			'Device': 'D',
			'Device_shifted': 'D',
			'User': 'U',
			'User_shifted': 'U',
			'Mod': 'M',
			'Select': 'C'}

_base_translations = {' ':42, '0': 0, '1': 1,'2': 2, '3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'A': 10,'B': 11,'C': 12,'D': 13,'E': 14,'F': 15,'G': 16,'H': 17,'I': 18,'J': 19,'K': 20,'L': 21,'M': 22,'N': 23,'O': 24,'P': 25,'Q': 26,'R': 27,'S': 28,'T': 29,'U': 30,'V': 31,'W': 32,'X': 33,'Y': 34,'Z': 35,'a': 10,'b': 11,'c': 12,'d': 13,'e': 14,'f': 15,'g': 16,'h': 17,'i': 18,'j': 19,'k': 20,'l': 21,'m': 22,'n': 23,'o': 24,'p': 25,'q': 26,'r': 27,'s': 28,'t': 29,'u': 30,'v': 31,'w': 32,'x': 33,'y': 34,'z': 35,'_': 39, '-': 42, '?': 127}


FADER_COLORS = [96, 124, 108, 120, 116, 100, 104, 112]

MIDIBUTTONMODE = (240, 0, 1, 97, 12, 66, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 247)
USERBUTTONMODE = (240, 0, 1, 97, 12, 66, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 247)
LIVEBUTTONMODE = (240, 0, 1, 97, 12, 66, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 247)
SPLITVERTICAL = (240, 0, 1, 97, 12, 66, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 5, 5, 5, 5, 247)
SPLITHORIZONTAL = (240, 0, 1, 97, 12, 66, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 247)

ATOFFBUTTONMODE = (240, 0, 1, 97, 12, 10, 36, 2, 37, 0, 38, 0, 39, 0, 40, 0, 41, 0, 42, 0, 43, 0, 44, 0, 45, 0, 46, 0, 47, 0, 48, 0, 49, 0, 50, 0, 51, 0, 52, 0, 53, 0, 54, 0, 55, 0, 56, 0, 57, 0, 58, 0, 59, 0, 60, 2, 61, 0, 62, 0, 63, 0, 64, 0, 65, 0, 66, 0, 67, 0, 247)
ATONBUTTONMODE = (240, 0, 1, 97, 12, 10, 36, 2, 37, 2, 38, 2, 39, 2, 40, 2, 41, 2, 42, 2, 43, 2, 44, 2, 45, 2, 46, 2, 47, 2, 48, 2, 49, 2, 50, 2, 51, 2, 52, 2, 53, 2, 54, 2, 55, 2, 56, 2, 57, 2, 58, 2, 59, 2, 60, 2, 61, 2, 62, 2, 63, 2, 64, 2, 65, 2, 66, 2, 67, 2, 247)

CLIPS_FADER_COLORS = tuple([240, 0, 1, 97, 12, 61, 7, 7, 7, 7, 7, 7, 7, 7, 2, 247])
SENDS_FADER_COLORS = tuple([240, 0, 1, 97, 12, 61, 5, 5, 5, 5, 4, 4, 4, 4, 2, 247])
DEVICE_FADER_COLORS = tuple([240, 0, 1, 97, 12, 61, 6, 6, 6, 6, 6, 6, 6, 6, 2, 247])
USER_FADER_COLORS =tuple([240, 0, 1, 97, 12, 61, 1, 1, 1, 1, 1, 1, 1, 1, 2, 247])
MOD_FADER_COLORS = tuple([240, 0, 1, 97, 12, 61, 7, 7, 7, 7, 7, 7, 7, 7, 2, 247])

STREAMINGON = (240, 0, 1, 97, 12, 62, 127, 247)
STREAMINGOFF = (240, 0, 1, 97, 12, 62, 0, 247)
LINKFUNCBUTTONS = (240, 0, 1, 97, 12, 68, 1, 247)
DISABLECAPFADERNOTES = (240, 0, 1, 97, 12, 69, 1, 247)
QUERYSURFACE = (240, 126, 127, 6, 1, 247)

MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE, MIDI_CC_TYPE, MIDI_PB_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224

_Q = Live.Song.Quantization
LAUNCH_QUANTIZATION = (_Q.q_quarter,
 _Q.q_half,
 _Q.q_bar,
 _Q.q_2_bars,
 _Q.q_4_bars,
 _Q.q_8_bars,
 _Q.q_8_bars,
 _Q.q_8_bars)

def is_device(device):
	return (not device is None and isinstance(device, Live.Device.Device) and hasattr(device, 'name'))


def make_pad_translations(chan):
	return tuple((x%4, int(x/4), x+16, chan) for x in range(16))


def return_empty():
	return []



class SendSysexMode(Mode):


	def __init__(self, script = None, sysex = None, *a, **k):
		super(SendSysexMode, self).__init__(*a, **k)
		self._send_midi = script._send_midi
		self._sysex = sysex
	

	def enter_mode(self):
		self._send_midi and self._send_midi(self._sysex)
	

	def leave_mode(self):
		pass
	


class BasePhysicalDisplayElement(PhysicalDisplayElement):


	def __init__(self, *a, **k):
		super(BasePhysicalDisplayElement, self).__init__(*a, **k)
		self._last_sent_messages = []
		self._message_clear_all = [tuple([176, 16, 127]), tuple([176, 17, 127])]
	

	def display_message(self, message):
		if not self._block_messages:
			message = str(message) + '  '
			self._message_to_send = [tuple(176, 16, self._translate_char(message[0])), tuple(176, 17, self._translate_char(message[1]))]
			self._request_send_message()
	

	def update(self):
		self._message_to_send = len(self._logical_segments) > 0 and not self._block_messages and None
		self._request_send_message()
	

	def clear_send_cache(self):
		self._last_sent_messages = []
		self._request_send_message()
	

	def reset(self):
		super(PhysicalDisplayElement, self).reset()
		if not self._block_messages:
			self._message_to_send = self._message_clear_all != None and self._message_clear_all
		self._request_send_message()
	

	def set_translation_table(self, translation_table):
		assert('?' in translation_table.keys())
		self._translation_table = translation_table
	

	def _send_message(self):
		if not self._block_messages:
			if self._message_to_send is None:
				self._message_to_send = self._build_message(map(first, self._central_resource.owners))
			self.send_midi(self._message_to_send)
	

	def send_midi(self, messages):
		if messages != self._last_sent_messages:
			for message in  messages:
				debug('sending message:', message)
				ControlElement.send_midi(self, message)
			self._last_sent_message = messages
	

	def _build_display_message(self, display):
		message = str(display.display_string) + ' '
		return message[0]
	

	def _build_message(self, displays):
		messages = []
		if len(displays) is 1:
			message = self._translate_string(' ' + str(displays[0].display_string))
			debug('message len:', len(message), 'message:', message)
			messages = [tuple([176, 34, message[-1]]), tuple([176, 35, message[-2]])]
		elif len(displays):
			for i in range(2):
				messages.append(tuple([176, 34 + i, self._translate_char(self._build_display_message(displays[i]))]))
		debug('messages to send:', messages)
		return messages
	



class BaseDisplayingModesComponent(ModesComponent):


	def __init__(self, *a, **k):
		super(BaseDisplayingModesComponent, self).__init__(*a, **k)
		self._mode_data_string = {}
		self._data_source = DisplayDataSource()
	

	def add_mode(self, name, mode_or_component, display_string = '', *a, **k):
		super(BaseDisplayingModesComponent, self).add_mode(name, mode_or_component, *a, **k)
		self._mode_data_string[name] = display_string
	

	def update(self, *a, **k):
		super(BaseDisplayingModesComponent, self).update(*a, **k)
		self._update_data_sources(self.selected_mode)
	

	def _do_enter_mode(self, name, *a, **k):
		super(BaseDisplayingModesComponent, self)._do_enter_mode(name, *a, **k)
		self._update_data_sources(name)
	

	def _update_data_sources(self, selected, *a, **k):
		if self.is_enabled():
			debug('setting data string to:', self._mode_data_string[selected])
			self._data_source.set_display_string(self._mode_data_string[selected])
	

	def set_display(self, display, *a, **k):
		if display:
			display.set_data_sources([self._data_source])
	


class BaseDeviceComponent(DeviceComponent):


	def update(self):
		super(BaseDeviceComponent, self).update()
		if self.is_enabled() and self._device != None:
			self._device_bank_registry.set_device_bank(self._device, self._bank_index)
			if self._parameter_controls != None:
				old_bank_name = self._bank_name
				self._assign_parameters()
				if self._bank_name != old_bank_name:
					self._show_msg_callback(self._device.name + ' Bank: ' + self._bank_name)
		elif self._parameter_controls != None:
			self._release_parameters(self._parameter_controls)
			for control in self._parameter_controls:
				if control:
					control.send_value(0, True)
		if self.is_enabled():
			self._update_on_off_button()
			self._update_lock_button()
			self._update_device_bank_buttons()
			self._update_device_bank_nav_buttons()
	


class MomentaryBehaviour(ModeButtonBehaviour):


	def press_immediate(self, component, mode):
		component.push_mode(mode)
	

	def release_immediate(self, component, mode):
		if len(component.active_modes) > 1:
			component.pop_mode(mode)
	

	def release_delayed(self, component, mode):
		if len(component.active_modes) > 1:
			component.pop_mode(mode)
	


class ExcludingMomentaryBehaviour(ExcludingBehaviourMixin, MomentaryBehaviour):


	def update_button(self, *a, **k):
		pass
	


class DelayedExcludingMomentaryBehaviour(ExcludingMomentaryBehaviour):


	def press_immediate(self, component, mode):
		pass
	

	def press_delayed(self, component, mode):
		component.push_mode(mode)
	


class CancellableBehaviourWithRelease(CancellableBehaviour):


	def release_delayed(self, component, mode):
		component.pop_mode(mode)
	


class ShiftedBehaviour(ModeButtonBehaviour):


	def __init__(self, color = 1, *a, **k):
		super(ShiftedBehaviour, self).__init__(*a, **k)
		self._color = color
		self._chosen_mode = None
	

	def press_immediate(self, component, mode):
		debug('selected_mode:', component.selected_mode, 'mode:', mode, 'chosen_mode:', self._chosen_mode,)
		if mode is component.selected_mode and not component.get_mode(mode+'_shifted') is None:
			self._chosen_mode = mode+'_shifted'
		else:
			self._chosen_mode = mode
		component.push_mode(self._chosen_mode)
	

	def release_immediate(self, component, mode):
		debug('chosen mode is:', self._chosen_mode)
		if component.selected_mode.endswith('_shifted'):
			component.pop_groups(['shifted'])
		elif len(component.active_modes) > 1:
			component.pop_unselected_modes()
	

	def release_delayed(self, component, mode):
		debug('chosen mode is:', self._chosen_mode)
		component.pop_mode(self._chosen_mode)
	

	def update_button(self, component, mode, selected_mode):
		button = component.get_mode_button(mode)
		groups = component.get_mode_groups(mode)
		selected_groups = component.get_mode_groups(selected_mode)
		#debug('--------mode:', mode, 'selected:', selected_mode, 'chosen:', self._chosen_mode)
		if mode == selected_mode:
			button.send_value(self._color, True)
		elif mode+'_shifted' == selected_mode:
			button.send_value(self._color + 7, True)
		else:
			button.send_value(0, True)
	


class LatchingShiftedBehaviour(ShiftedBehaviour):


	def press_immediate(self, component, mode):
		#debug('mode button for ->', mode, 'currently selected_mode:', component.selected_mode, 'last chosen mode:', self._chosen_mode)
		if mode is component.selected_mode and component.get_mode(mode+'_shifted'):
			self._chosen_mode = mode+'_shifted'
		#elif (component.selected_mode != mode + '_shifted') and (self._chosen_mode != mode + '_shifted'):
		#	component.pop_groups(['shifted'])
		#	self._chosen_mode = mode
		else:
			self._chosen_mode = mode
		component.push_mode(self._chosen_mode)
		debug('new chosen_mode:', self._chosen_mode,)
	

	def release_immediate(self, component, mode):
		if len(component.active_modes) > 1:
			component.pop_unselected_modes()
		#debug('selected mode:', component.selected_mode)
	

	def release_delayed(self, component, mode):
		if not mode is self._chosen_mode is mode + '_shifted':
			if len(component.active_modes) > 1:
				component.pop_mode(component.selected_mode)
		#debug('selected mode:', component.selected_mode)
	


class FlashingBehaviour(CancellableBehaviourWithRelease):


	def __init__(self, color = 1, *a, **k):
		super(FlashingBehaviour, self).__init__(*a, **k)
		self._color = color
	

	def update_button(self, component, mode, selected_mode):
		button = component.get_mode_button(mode)
		groups = component.get_mode_groups(mode)
		selected_groups = component.get_mode_groups(selected_mode)
		if mode == selected_mode or bool(groups & selected_groups):
			button.send_value(self._color + 7, True)
		else:
			button.send_value(self._color, True)
	


class BaseSessionRecordingComponent(FixedLengthSessionRecordingComponent):


	def __init__(self, *a, **k):
		self._length_value = 1
		super(BaseSessionRecordingComponent, self).__init__(*a, **k)
		self._length_buttons = []
	

	def _get_selected_length(self):
		song = self.song()
		length = 2.0 ** (LENGTH_VALUES[self._length_value])
		quant = LAUNCH_QUANTIZATION[(LENGTH_VALUES[self._length_value])]
		#if self._length_value > 1:
		length = length * song.signature_numerator / song.signature_denominator
		return (length, quant)
	

	def set_length_buttons(self, buttons):
		self._on_length_buttons_value.subject = buttons
		self.update_length_buttons()
	

	@subject_slot('value')
	def _on_length_buttons_value(self, value, x, y, *a, **k):
		if value > 0:
			self._length_value = x
			self.update_length_buttons()
	

	def update(self, *a, **k):
		super(BaseSessionRecordingComponent, self).update(*a, **k)
		if self.is_enabled():
			self.update_length_buttons()
	

	def update_length_buttons(self):
		buttons = self._on_length_buttons_value.subject
		if buttons:
			for button, (x, y) in buttons.iterbuttons():
				if button:
					if x == self._length_value:
						button.turn_on()
					else:
						button.turn_off()
	


class BlockingMonoButtonElement(MonoButtonElement):


	def __init__(self, *a, **k):
		super(BlockingMonoButtonElement, self).__init__(*a, **k)
		self._is_held = False
		self._held_value = 1
		self.display_press = False
		self._last_flash = 0
		self.scale_color = 0
		self._skin_colors = {'NoteEditor.Step.Low':3, 'NoteEditor.Step.High':1, 'NoteEditor.Step.Full':2, 'NoteEditor.Step.Muted':3, 'NoteEditor.Step.Empty':0,
								'NoteEditor.StepLow':3, 'NoteEditor.StepHigh':1, 'NoteEditor.StepFull':2, 'NoteEditor.StepMuted':3, 'NoteEditor.StepEmpty':0, 'NoteEditor.StepEditing.High':6,
								'NoteEditor.StepEmptyBase':0, 'NoteEditor.StepEmptyScale':0, 'NoteEditor.StepDisabled':0, 'NoteEditor.Playhead':2, 
								'NoteEditor.StepSelected':6, 'NoteEditor.PlayheadRecord':5, 'NoteEditor.QuantizationSelected':5, 'NoteEditor.QuantizationUnselected':4,
								'LoopSelector.Playhead':2, 'LoopSelector.OutsideLoop':7, 'LoopSelector.InsideLoopStartBar':3, 'LoopSelector.SelectedPage':1, 
								'LoopSelector.InsideLoop':3, 'LoopSelector.PlayheadRecord':5, 
								'DrumGroup.PadAction':1, 'DrumGroup.PadFilled':6, 'DrumGroup.PadSelected':1, 'DrumGroup.PadEmpty':0, 'DrumGroup.PadMuted':2, 
								'DrumGroup.PadSoloed':3, 'DrumGroup.PadMutedSelected':7, 'DrumGroup.PadSoloedSelected':7,
								 }

	

	"""def install_connections(self):
		if self._is_enabled:
			ButtonElement.install_connections(self)
		elif ((self._msg_channel != self._original_channel) or (self._msg_identifier != self._original_identifier)):
			self._install_translation(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)
			#self._install_original_forwarding(self)"""
	

	def press_flash(self, value, force = False):
		assert (value != None)
		assert isinstance(value, int)
		assert (value in range(128))
		#self._script.log_message('blockbutton:' + str(self._original_identifier))
		if self.display_press and (not value is self._last_flash or force):
			data_byte1 = self._original_identifier
			if value == 0:
				if self.scale_color is 127:
					data_byte2 = COLOR_MAP[-1]
				elif self.scale_color is 0:
					data_byte2 = 0
				else:
					data_byte2 = COLOR_MAP[max(0, (self.scale_color-1)%7)]
			else:
				data_byte2 = 1
			status_byte = self._original_channel
			status_byte +=	144
			self.send_midi((status_byte, data_byte1, data_byte2))
			self._last_flash = value
	

	def set_light(self, value):
		if value is True:
			self.send_value(self._on_value)
		elif value is False:
			self.send_value(self._off_value)
		elif value in self._skin_colors.keys():
			self.send_value(self._skin_colors[value])
		else:
			self._script.log_message('skin color: ' + str(value))
			self.send_value(len(value))
	

	def set_on_off_values(self, on_value, off_value):
		if not on_value in range(128):
			if on_value in self._skin_colors.keys():
				on_value = self._skin_colors[on_value]
			else:
				#self._script.log_message('on_value skin color: ' + str(on_value))
				on_value = len(on_value)
		if not off_value in range(128):
			if off_value in self._skin_colors.keys():
				off_value = self._skin_colors[off_value]
			else:
				#self._script.log_message('off_value skin color: ' + str(off_value))
				off_value = len(off_value)
		super(BlockingMonoButtonElement, self).set_on_off_values(on_value, off_value)
	


class BaseMixerComponent(MixerComponent):


	def __init__(self, script, *a, **k):
		super(BaseMixerComponent,self).__init__( *a, **k)
		self._script = script
	

	def _create_strip(self):
		return BaseChannelStripComponent()
	

	def set_next_track_button(self, next_button):
		if next_button is not self._next_track_button:
			self._next_track_button = next_button
			self._next_track_button_slot.subject = next_button
			self.on_selected_track_changed()
	

	def set_previous_track_button(self, prev_button):
		if prev_button is not self._prev_track_button:
			self._prev_track_button = prev_button
			self._prev_track_button_slot.subject = prev_button
			self.on_selected_track_changed()
	

	def set_return_controls(self, controls):
		for strip, control in map(None, self._return_strips, controls or []):
			strip.set_volume_control(control)
	

	def tracks_to_use(self):
		return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)
	


class BaseChannelStripComponent(ChannelStripComponent):


	def set_stop_button(self, button):
		self._on_stop_value.subject = button
	

	@subject_slot('value')
	def _on_stop_value(self, value):
		if self._track:
			self._track.stop_all_clips()
	

	def set_invert_mute_feedback(self, invert_feedback):
		assert(isinstance(invert_feedback, type(False)))
		self._invert_mute_feedback = invert_feedback
		self.update()
	

	def _on_mute_changed(self):
		if self.is_enabled() and self._mute_button != None:
			if self._track != None or self.empty_color == None:
				if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute == self._invert_mute_feedback:
					self._mute_button.turn_on()
				else:
					self._mute_button.turn_off()
			else:
				self._mute_button.set_light(self.empty_color)
	


class BaseModeSelector(ModeSelectorComponent):


	def __init__(self, script):
		super(BaseModeSelector, self).__init__()
		self._held = None
		self._script = script
		self._set_protected_mode_index(0)	
	

	def number_of_modes(self):
		return 4
	

	def _mode_value(self, value, sender):
		#if sender in (self._modes_buttons[1], self._modes_buttons[2]):
			#if not sender is self._held and not self._script.pad_held()):
		if not sender is self._held:
			if not self._script.pad_held() or sender in (self._modes_buttons[1], self._modes_buttons[2]):
				if value:
					super(BaseModeSelector, self)._mode_value(value, sender)
					self._held = sender
					self._script._shift_update(self._mode_index, not self._held is None)
					self._script.schedule_message(3, self._script._check_mode_shift, self._held)
		elif value is 0:
			#else:
			self._held = None
			self._script._shift_update(self._mode_index, not self._held is None)
	

	def update(self):
		if self._is_enabled:
			buttons = self._modes_buttons
			for index in range(len(buttons)):
				if index == self._mode_index:
					buttons[index].turn_on(True)
				else:
					buttons[index].turn_off(True)
			#for index in range(8):
				#self._script._send_midi((191, index+1, LAYERSPLASH[self._mode_index]))
	

	def is_shifted(self):
		return not self._held is None
	

	"""def set_mode_buttons(self, buttons):
		for button in self._modes_buttons:
			button.remove_value_listener(self._mode_value)
		self._modes_buttons = []
		if (buttons != None):
			for button in buttons:
				assert isinstance(button, MonoButtonElement)
				identify_sender = True
				button.add_value_listener(self._mode_value, identify_sender)
				self._modes_buttons.append(button)
			for index in range(len(self._modes_buttons)):
				if (index == self._mode_index):
					self._modes_buttons[index].turn_on()
				else:
					self._modes_buttons[index].turn_off()"""
	


class BaseUserModeSelector(ModeSelectorComponent):


	def __init__(self, script):
		super(BaseUserModeSelector, self).__init__()
		self._held = None
		self._script = script
		self._set_protected_mode_index(0)	
	

	def number_of_modes(self):
		return 8
	

	def _mode_value(self, value, sender):
		if self._is_enabled:
			if not sender is self._held:
				super(BaseUserModeSelector, self)._mode_value(value, sender)
				self._held = sender
			elif value is 0:
				self._held = None
			self._script._user_shift_update(self._mode_index, not self._held is None)
	

	def update(self):
		if self._is_enabled:
			buttons = self._modes_buttons
			for index in range(len(buttons)):
				if index == self._mode_index:
					buttons[index].turn_on(True)
				else:
					buttons[index].turn_off(True)
	

	def is_shifted(self):
		return not self._held is None
	


class BaseMidiModeSelector(ModeSelectorComponent):


	def __init__(self, callback):
		super(BaseMidiModeSelector, self).__init__()
		self._report_mode = callback
		self._set_protected_mode_index(0)	
	

	def number_of_modes(self):
		return 2
	

	def _mode_value(self, value, sender):
		if self._is_enabled:
			super(BaseMidiModeSelector, self)._mode_value(value, sender)
			self._report_mode(self._mode_index)
	

	def update(self):
		if self._is_enabled:
			for index in range(len(self._modes_buttons)):
				if self._mode_index == index:
					self._modes_buttons[index].turn_on(True)
				else:
					self._modes_buttons[index].turn_off(True)
	


class BaseSessionComponent(SessionComponent):


	def __init__(self, num_tracks, num_scenes):
		super(BaseSessionComponent, self).__init__(num_tracks, num_scenes)
	

	def set_clip_launch_buttons(self, buttons):
		assert(not buttons or (buttons.width() <= self._num_tracks and buttons.height() <= self._num_scenes))
		if buttons:
			for button, (x, y) in buttons.iterbuttons():
				if button:
					button.set_off_value(0)
				scene = self.scene(y)
				slot = scene.clip_slot(x)
				slot.set_launch_button(button)

		else:
			for x, y in product(xrange(self._num_tracks), xrange(self._num_scenes)):
				scene = self.scene(y)
				slot = scene.clip_slot(x)
				slot.set_launch_button(None)
	

	def set_scene_launch_buttons(self, buttons):
		assert(not buttons or (buttons.height() == self._num_scenes and buttons.width() == 1))
		if buttons:
			for button, (_, x) in buttons.iterbuttons():
				scene = self.scene(x)
				scene.set_launch_button(button)
				if button:
					button.send_value(7, True)

		else:
			for x in xrange(self._num_scenes):
				scene = self.scene(x)
				scene.set_launch_button(None)
	


class BaseFaderArray(Array):


	def __init__(self, name, size, active_handlers = return_empty):
		self._active_handlers = active_handlers
		self._name = name
		self._cell = [StoredElement(self._name + '_' + str(num), _num = num, _mode = 1, _value = 7) for num in range(size)]
	

	def value(self, num, value = 0):
		element = self._cell[num]
		element._value = value % 8
		self.update_element(element)
	

	def mode(self, num, mode = 0):
		element = self._cell[num]
		element._mode = mode % 4
		self.update_element(element)
	

	def update_element(self, element):	
		for handler in self._active_handlers():
			handler.receive_address(self._name, element._num, (FADER_COLORS[element._value]) + element._mode )
	


class StoredControlElement(StoredElement):


	def __init__(self, *a, **k):
		self._id = -1
		self._channel = -1
		super(StoredControlElement, self).__init__(*a, **k)
	

	def id(self, id):
		self._id = id
		self.update_element()
	

	def channel(self, channel):
		self._channel = channel
		self.udpate_element()
	


class BaseGrid(Grid):


	def __init__(self, name, width, height, active_handlers = return_empty, *a, **k):
		super(BaseGrid, self).__init__(name, width, height, active_handlers = return_empty, *a, **k)
		self._cell = [[StoredControlElement(active_handlers, _name = self._name + '_' + str(x) + '_' + str(y), _x = x, _y = y, ) for y in range(height)] for x in range(width)]
	

	def id(self, x, y, identifier = -1):
		element = self._cell[x][y]
		element._id = min(127, max(-1, identifier))
		self.update_element(element)
	

	def channel(self, x, y, channel = -1):
		element = self._cell[x][y]
		element._channel = min(15, max(-1, channel))
		self.update_element(element)
	

	def update_element(self, element):
		for handler in self._active_handlers():
			handler.receive_address(self._name, element._x, element._y, value = element._value, id = element._id, channel = element._channel)
	


class BaseModHandler(ModHandler):


	def __init__(self, *a, **k):
		self._base_grid = None
		self._base_grid_CC = None
		self._fader_color_override = False
		addresses = {'base_grid': {'obj': BaseGrid('base_grid', 8, 4), 'method':self._receive_base_grid},
					'base_fader': {'obj': BaseFaderArray('base_fader', 8), 'method':self._receive_base_fader}}
		super(BaseModHandler, self).__init__(addresses = addresses, *a, **k)
		self._is_shifted = False
		self.nav_box = self.register_component(NavigationBox(self, 16, 16, 2, 2, self.set_offset))
	

	def _receive_base_grid(self, x, y, *a, **k):
		#self.log_message('_receive_base_grid: %s %s %s %s' % (x, y, value, is_id))
		if self._active_mod and not self._active_mod.legacy and self._base_grid_value.subject:
			keys = k.keys()
			if 'value' in keys:
				self._base_grid_value.subject.send_value(x, y, k['value'], True)
			if 'id' in keys or 'channel' in keys:
				button = self._base_grid_value.subject.get_button(x, y)
				if 'id' in keys:
					id = k['id']
					if id < 0:
						button.set_identifier(button._original_identifier)
					else:
						button.set_identifier(id)
				if 'channel' in keys:
					channel = k['channel']
					if channel < 0:
						button.set_channel(button._original_channel)
					else:
						button.set_channel(channel)
				button.set_enabled(button._msg_identifier == button._original_identifier and button._msg_channel == button._original_channel)
	

	def _receive_base_fader(self, num, value):
		#self.log_message('_receive_base_fader: %s %s' % (num, value))
		if self.is_enabled():
			self._script._send_midi((191, num+10, value))
	

	def _receive_shift(self, value):
		pass
	

	def _receive_grid(self, x, y, value, is_id = False):
		#self.log_message('receive grid')
		if self._active_mod and self._active_mod.legacy:
			if not self._base_grid_value.subject is None:
				if (x - self.x_offset) in range(8) and (y - self.y_offset) in range(4):
					self._base_grid_value.subject.send_value(x - self.x_offset, y - self.y_offset, value, True)
	

	def set_base_grid(self, grid):
		debug('set base grid:', grid)
		old_grid = self._base_grid_value.subject
		if old_grid:
			for button, _ in old_grid.iterbuttons():
				button.use_default_message() 
		self._base_grid = grid
		self._base_grid_value.subject = self._base_grid
	

	def set_base_grid_CC(self, grid):
		self._base_grid_CC = grid
		self._base_grid_CC_value.subject = self._base_grid_CC
	

	@subject_slot('value')
	def _keys_value(self, value, x, y, *a, **k):
		self.active_mod() and self.active_mod().send('key', x, value)
	

	@subject_slot('value')
	def _base_grid_value(self, value, x, y, *a, **k):
		#self.log_message('_base_grid_value ' + str(x) + str(y) + str(value))
		mod = self.active_mod()
		if mod:
			if mod.legacy:
				mod.send('grid', x + self.x_offset, y + self.y_offset, value)
			else:
				mod.send('base_grid', x, y, value)
		
	

	@subject_slot('value')
	def _base_grid_CC_value(self, value, x, y, *a, **k):
		#self.log_message('_base_grid_CC_value ' + str(x) + str(y) + str(value))
		mod = self.active_mod()
		if mod:
			if mod.legacy:
				mod.send('grid_CC', x + self.x_offset , y + self.y_offset, value)
			else:
				mod.send('base_grid_CC', x, y, value)
	

	@subject_slot('value')
	def _shift_value(self, value, *a, **k):
		self._is_shifted = not value is 0
		mod = self.active_mod()
		if mod:
			mod.send('shift', value)
		if self._is_shifted:
			self.shift_layer.enter_mode()
			if mod and mod.legacy:
				self.legacy_shift_layer.enter_mode()
		else:
			self.legacy_shift_layer.leave_mode()
			self.shift_layer.leave_mode()
		self.update()
	

	def update(self, *a, **k):
		mod = self.active_mod()
		if mod:
			mod.restore()
			if mod.legacy and self._shift_value.subject and self._shift_value.subject.is_pressed():
				self._display_nav_box()
		else:
			if not self._base_grid_value.subject is None:
				self._base_grid_value.subject.reset()
			if not self._keys_value.subject is None:
				self._keys_value.subject.reset()
			#self.update_device()
	


class BaseMonoInstrumentComponent(MonoInstrumentComponent):


	def set_shift_button(self, button):
		self._shifted = 0
		self._drumpad._step_sequencer._drum_group._select_button = button  #drum_group uses is_pressed() to determine an action
	


class BaseM4LInterfaceComponent(ControlSurfaceComponent, ControlElementClient):
	"""
	Simplified API for interaction from M4L as a high priority layer
	superposed on top of any functionality.
	"""


	def __init__(self, controls = None, component_guard = None, priority = 1, *a, **k):
		super(BaseM4LInterfaceComponent, self).__init__(self, *a, **k)
		self._priority = priority
		self._controls = dict(map(lambda x: (x.name, x), controls))
		self._grabbed_controls = []
		self._component_guard = component_guard
	

	def disconnect(self):
		for control in self._grabbed_controls[:]:
			self.release_control(control)
		super(BaseM4LInterfaceComponent, self).disconnect()
	

	def set_control_element(self, control, grabbed):
		if hasattr(control, 'release_parameter'):
			control.release_parameter()
		control.reset()
	

	def get_control_names(self):
		return self._controls.keys()
	

	def get_control(self, control_name):
		return self._controls[control_name] if control_name in self._controls else None
	

	def grab_control(self, control):
		assert(control in self._controls.values())
		with self._component_guard():
			if control not in self._grabbed_controls:
				control.resource.grab(self, priority=self._priority)
				self._grabbed_controls.append(control)
	

	def release_control(self, control):
		assert(control in self._controls.values())
		with self._component_guard():
			if control in self._grabbed_controls:
				self._grabbed_controls.remove(control)
				control.resource.release(self)
	


class Base(ControlSurface):
	__module__ = __name__
	__doc__ = " Base controller script "


	def __init__(self, c_instance):
		super(Base, self).__init__(c_instance)
		self._connected = False
		self._host_name = 'Base'
		self._color_type = 'OhmRGB'
		self.monomodular = None
		self.oscServer = None
		self._rgb = 0
		self._timer = 0
		self._current_nav_buttons = []
		self.flash_status = 1
		self._touched = 0
		self._last_pad_stream = [0 for i in range(0, 32)]
		self._shift_latching = LatchingShiftedBehaviour if SHIFT_LATCHING else ShiftedBehaviour
		with self.component_guard():
			self._setup_monobridge()
			if OSC_TRANSMIT:
				self._setup_OSC_layer()
			self._setup_controls()
			self._define_sysex()
			self._setup_display()
			self._setup_autoarm()
			self._setup_mixer_control()
			self._setup_session_control()
			self._setup_transport_control()
			self._setup_device_control()
			self._setup_session_recording_component()
			self._setup_translations()
			self._setup_instrument()
			self._setup_mod()
			self._setup_modswitcher()
			self._setup_main_modes()
			self._setup_m4l_interface()
			self._device_selection_follows_track_selection = True
			self._on_device_changed.subject = self.song()
			self.set_feedback_channels(range(14, 15))
		self.log_message("<<<<<<<<<<<<<<<<<= Base log opened =>>>>>>>>>>>>>>>>>>>>>") 
		self.schedule_message(3, self._check_connection)
	

	def set_feedback_channels(self, channels, *a, **k):
		debug('set feedback channels: ' + str(channels))
		super(Base, self).set_feedback_channels(channels, *a, **k)
	

	"""script initialization methods"""
	def _initialize_hardware(self):
		#self._send_sysex((240, 0, 1, 97, 12, 22, 16, 247))
		self._send_midi(STREAMINGON)
		self._send_midi(LINKFUNCBUTTONS)
		self._send_midi(DISABLECAPFADERNOTES)
		self._send_midi((191, 122, 64))
	

	def _check_connection(self):
		if not self._connected:
			self._send_midi(QUERYSURFACE)
			self.schedule_message(100, self._check_connection)
	

	def _setup_monobridge(self):
		self._monobridge = MonoBridgeElement(self)
		self._monobridge.name = 'MonoBridge'
	

	def pad_held(self):
		return (sum(self._last_pad_stream)>0)
	

	def _setup_controls(self):
		is_momentary = True
		self._fader = [MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, BASE_TOUCHSTRIPS[index], Live.MidiMap.MapMode.absolute, 'Fader_' + str(index), index, self) for index in range(9)]
		for fader in self._fader:
			fader._mapping_feedback_delay = -1
		self._fader_matrix = ButtonMatrixElement(name = 'FaderMatrix', rows = [self._fader[:8]])
		self._button = [MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_BUTTONS[index], 'Button_' + str(index), self) for index in range(8)]
		self._pad = [BlockingMonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_PADS[index],	 'Pad_' + str(index), self) for index in range(32)]
		self._pad_doublepress = [DoublePressElement(pad) for pad in self._pad]
		self._pad_CC = [MonoEncoderElement(MIDI_CC_TYPE, CHANNEL, BASE_PADS[index], Live.MidiMap.MapMode.absolute, 'Pad_CC_' + str(index), index, self) for index in range(32)]
		self._touchpad = [MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_TOUCHPADS[index], 'TouchPad_' + str(index), self, resource_type = PrioritizedResource) for index in range(8)]
		self._touchpad_matrix = ButtonMatrixElement(name = 'TouchPadMatrix', rows = [self._touchpad],)
		self._touchpad_multi = MultiElement(self._touchpad[0], self._touchpad[1], self._touchpad[2], self._touchpad[3], self._touchpad[4], self._touchpad[5], self._touchpad[6], self._touchpad[7],)
		self._runner = [MonoButtonElement(is_momentary, MIDI_NOTE_TYPE, CHANNEL, BASE_RUNNERS[index], 'Runner_' + str(index), self) for index in range(8)]
		self._runner_matrix = ButtonMatrixElement(name = 'RunnerMatrix', rows = [self._runner])
		self._stream_pads = [self._pad[index%8 + (abs((index/8)-3)*8)] for index in range(32)]
		self._nav_buttons = ButtonMatrixElement( name = 'nav_buttons' )
		self._nav_buttons.add_row(self._button[4:8])
		self._on_nav_button_value.subject = self._nav_buttons
		self._base_grid = ButtonMatrixElement()
		self._base_grid.name = 'BaseGrid'
		self._base_grid_CC = ButtonMatrixElement()
		self._base_grid_CC.name = 'BaseGridCC'
		self._keys = ButtonMatrixElement(name = 'Keys')
		self._keys_display = ButtonMatrixElement(name = 'KeysDisplay')
		for index in range(4):
			self._base_grid.add_row(self._pad[(index*8):(index*8)+8])
			self._base_grid_CC.add_row(self._pad_CC[(index*8):(index*8)+8])
		self._base_doublepress_grid = ButtonMatrixElement(name = 'doublepress_matrix', rows = [[self._pad_doublepress[column+(row*8)] for column in range(8)] for row in range(4)])
		self._keys.add_row(self._touchpad[0:8])
		self._keys_display.add_row(self._runner[0:8])
		self._drumpad_grid = ButtonMatrixElement(name = 'DrumPadGrid')
		for index in range(4):
			self._drumpad_grid.add_row(self._pad[(index*8):(index*8)+4])
		self._up_button = self._nav_buttons[UDLR[0]]
		self._dn_button = self._nav_buttons[UDLR[1]]
		self._lt_button = self._nav_buttons[UDLR[2]]
		self._rt_button = self._nav_buttons[UDLR[3]]

		"""We'll use this to store descriptor strings of control functions so we can send them to an LCD application"""
		for button in self._button:
			button._descriptor = 'None'
		for touchpad in self._touchpad:
			touchpad._descriptor = 'None'
		for pad in self._pad:
			pad._descriptor = 'None'
	

	def _define_sysex(self):
		self.clips_layer_sysex = SendSysexMode(script = self, sysex = CLIPS_FADER_COLORS)
		self.sends_layer_sysex = SendSysexMode(script = self, sysex = SENDS_FADER_COLORS)
		self.device_layer_sysex = SendSysexMode(script = self, sysex = DEVICE_FADER_COLORS)
		self.user_layer_sysex = SendSysexMode(script = self, sysex = USER_FADER_COLORS)
		self.mod_layer_sysex = SendSysexMode(script = self, sysex = USER_FADER_COLORS)

		self.midi_mode_sysex = SendSysexMode(script = self, sysex = MIDIBUTTONMODE)
		self.user_mode_sysex = SendSysexMode(script = self, sysex = USERBUTTONMODE)
		self.live_mode_sysex = SendSysexMode(script = self, sysex = LIVEBUTTONMODE)
		self.splitvertical_mode_sysex = SendSysexMode(script = self, sysex = SPLITVERTICAL)
		self.splithorizontal_mode_sysex = SendSysexMode(script = self, sysex = SPLITHORIZONTAL)
		self.atoff_mode_sysex = SendSysexMode(script = self, sysex = ATOFFBUTTONMODE)
		self.aton_mode_sysex = SendSysexMode(script = self, sysex = ATONBUTTONMODE)
	

	def _setup_display(self):
		self._display = BasePhysicalDisplayElement(width_in_chars = 2)
		self._display.name = 'Display'
		self._display.set_message_parts(header = [176, 34,], tail = [])
		self._display.set_clear_all_message((176, 34, 127, 176, 35, 127))
		self._display.set_translation_table(_base_translations)
	
	
	def _setup_autoarm(self):
		self._auto_arm = AutoArmComponent(name='Auto_Arm')
		self._auto_arm.can_auto_arm_track = self._can_auto_arm_track
	

	def _setup_mixer_control(self):
		is_momentary = True
		self._num_tracks = (8) #A mixer is one-dimensional; 
		self._mixer = BaseMixerComponent(script = self, num_tracks = 8, num_returns = 4, invert_mute_feedback = True, autoname = True)
		self._mixer.name = 'Mixer'
		self._mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
		self._mixer.master_strip().set_volume_control(self._fader[8])
		self._mixer.volume_layer = AddLayerMode(self._mixer, Layer(priority = 4, volume_controls = self._fader_matrix))
		self._mixer.select_layer = AddLayerMode(self._mixer, Layer(priority = 4, track_select_buttons = self._touchpad_matrix))
		selected_strip = self._mixer.selected_strip()
		self._mixer.selected_channel_controls_layer = DelayMode(AddLayerMode(selected_strip, Layer(priority = 9, arm_button = self._button[6], solo_button = self._button[5], mute_button = self._button[4], stop_button = self._button[7])))
		self._mixer.selected_sends_layer = AddLayerMode(selected_strip, Layer(priority = 4, send_controls = self._fader_matrix.submatrix[:4, :]))
		self._mixer.returns_layer = AddLayerMode(self._mixer, Layer(priority = 4, return_controls = self._fader_matrix.submatrix[4:, :]))
		self._mixer.channel_controls_layer = AddLayerMode(self._mixer, Layer(priority = 4, arm_buttons = self._base_grid.submatrix[:, 2:3],
																		mute_buttons = self._base_grid.submatrix[:, :1],
																		solo_buttons = self._base_grid.submatrix[:, 1:2],))
		self._mixer.navigation_layer = AddLayerMode(self._mixer, Layer(priority = 6, previous_track_button = self._button[6], next_track_button = self._button[7]))
		self.song().view.selected_track = self._mixer.channel_strip(0)._track 
		self._mixer.set_enabled(True)
	

	def _setup_session_control(self):
		self._session = BaseSessionComponent(8, 4)
		self._session.name = "Session"
		self._session.set_offsets(0, 0)	 
		self._session.set_stop_clip_value(STOP_CLIP)
		self._scene = [None for index in range(4)]
		for row in range(4):
			self._scene[row] = self._session.scene(row)
			self._scene[row].name = 'Scene_' + str(row)
			for column in range(8):
				clip_slot = self._scene[row].clip_slot(column)
				clip_slot.name = str(column) + '_Clip_Slot_' + str(row)
				clip_slot.set_triggered_to_play_value(CLIP_TRG_PLAY)
				clip_slot.set_triggered_to_record_value(CLIP_TRG_REC)
				clip_slot.set_stopped_value(CLIP_STOP)
				clip_slot.set_started_value(CLIP_STARTED)
				clip_slot.set_recording_value(CLIP_RECORDING)
		self._session.set_mixer(self._mixer)
		self._session.cliplaunch_layer = AddLayerMode(self._session, Layer(priority = 4, clip_launch_buttons = self._base_grid))
		self._session.overlay_cliplaunch_layer = DelayMode(AddLayerMode(self._session, Layer(priority = 9, clip_launch_buttons = self._base_grid.submatrix[:7, :], scene_launch_buttons = self._base_grid.submatrix[7:, :])))
		self._session.navigation_layer = AddLayerMode(self._session, Layer(priority = 6, scene_bank_up_button = self._button[4], scene_bank_down_button = self._button[5], track_bank_left_button = self._button[6], track_bank_right_button = self._button[7]))
		#self._session.selected_stop_control = AddLayerMode(self._session, Layer(priority = 9, 
		#self._session.set_track_banking_increment(TRACK_BANKING_INCREMENT)	 #this function was removed from the session component :(
		self.set_highlighting_session_component(self._session)
		self._session._do_show_highlight()
	

	def _setup_transport_control(self):
		self._transport = TransportComponent()
		self._transport.name = 'Transport'
		self._transport.overdub_layer = AddLayerMode(self._transport, Layer(priority = 5, overdub_button = self._button[4]))
	

	def _setup_device_control(self):
		self._device = BaseDeviceComponent()
		self._device.name = 'Device_Component'
		self._device.parameters_layer = AddLayerMode(self._device, Layer(priority = 4, parameter_controls = self._fader_matrix.submatrix[:8][:]))
		self._device.nav_layer = AddLayerMode(self._device, Layer(priority = 5, bank_prev_button = self._button[4], bank_next_button = self._button[5]))
		self.set_device_component(self._device)
		self._device_navigator = DeviceNavigator(self._device, self._mixer, self)
		self._device_navigator.name = 'Device_Navigator'
		self._device_navigator.main_layer = AddLayerMode(self._device_navigator, Layer(priority = 6, prev_button = self._button[4], next_button = self._button[5]))
		self._device_navigator.alt_layer = AddLayerMode(self._device_navigator, Layer(priority = 6, prev_chain_button = self._button[4], next_chain_button = self._button[5], enter_button = self._button[6], exit_button = self._button[7]))
		self._device_selection_follows_track_selection = FOLLOW 
		self._device.device_name_data_source().set_update_callback(self._on_device_name_changed)
	

	def _setup_session_recording_component(self):
		self._clip_creator = ClipCreator()
		self._clip_creator.name = 'ClipCreator'
		self._recorder = BaseSessionRecordingComponent(self._clip_creator, ViewControlComponent())
		self._recorder.main_layer = LayerMode(self._recorder, Layer(priority = 5, new_button = self._button[5], record_button = self._button[6], length_button = self._button[7]))
		self._recorder.alt_layer = LayerMode(self._recorder, Layer(priority = 5, length_buttons = self._nav_buttons.submatrix[1:4][:]))
		self._recorder.set_enabled(True)
	

	def _setup_m4l_interface(self):
		self._m4l_interface = BaseM4LInterfaceComponent(controls=self.controls, component_guard=self.component_guard, priority = 10)
		self._m4l_interface.name = "M4LInterface"
		self.get_control_names = self._m4l_interface.get_control_names
		self.get_control = self._m4l_interface.get_control
		self.grab_control = self._m4l_interface.grab_control
		self.release_control = self._m4l_interface.release_control
	

	def _setup_translations(self):
		controls = []
		for button, _ in self._base_grid.iterbuttons():
			controls.append(button)
		for fader, _ in self._fader_matrix.iterbuttons():
			controls.append(fader)
		self._translations = TranslationComponent(controls, 10)
		self._translations.name = 'TranslationComponent'
		self._translations.layer = Layer(priority = 10, channel_selector_buttons = self._nav_buttons)
		self._translations.set_enabled(False)
	

	def _setup_mod(self):
		self.monomodular = get_monomodular(self)
		self.monomodular.name = 'monomodular_switcher'
		self.modhandler = BaseModHandler(script = self) #detect_mod = self._on_new_device_set)
		self.modhandler.name = 'ModHandler'
		self.modhandler.layer = Layer(priority = 6, base_grid = self._base_grid, 
													base_grid_CC = self._base_grid_CC,
													key_buttons = self._runner_matrix,
													parameter_controls = self._fader_matrix,
													alt_button = self._button[6],
													lock_button = self._button[7],)
		self.modhandler.alt_layer = AddLayerMode(self.modhandler, Layer(priority = 8,
													device_selector_matrix = self._touchpad_matrix,))
		self.modhandler.legacy_shift_layer = AddLayerMode(self.modhandler, Layer(priority = 7,
													channel_buttons = self._base_grid.submatrix[:6, :1],
													nav_matrix = self._base_grid.submatrix[6:8, :],))
		self.modhandler.shift_layer = AddLayerMode(self.modhandler, Layer(priority = 7,
													key_buttons = self._touchpad_matrix,))
		self.modhandler.set_enabled(False)
	

	def _setup_instrument(self):
		self._grid_resolution = self.register_disconnectable(GridResolution())
		self._c_instance.playhead.enabled = True
		self._playhead_element = PlayheadElement(self._c_instance.playhead)
		self._playhead_element.reset()
		self._skin = make_default_skin()

		quantgrid = ButtonMatrixElement([self._base_grid._orig_buttons[2][4:8], self._base_grid._orig_buttons[3][4:7]])

		self._instrument = BaseMonoInstrumentComponent(self, self._skin, grid_resolution = self._grid_resolution,) # modhandler = self.modhandler )
		self._instrument.name = 'InstrumentModes'
		self._instrument.layer = Layer(priority = 5) #button_matrix = self._base_grid)
		self._instrument.audioloop_layer = LayerMode(self._instrument, Layer(priority = 6, loop_selector_matrix = self._base_grid))
		self._instrument.octave_toggle = AddLayerMode(self._instrument, Layer(octave_enable_button = self._button[4]))
		self._instrument.shift_button1 = AddLayerMode(self._instrument, Layer(shift_button = self._button[1]))
		self._instrument.shift_button2 = AddLayerMode(self._instrument, Layer(shift_button = self._button[2]))
		self._instrument.keypad_shift_layer = AddLayerMode(self._instrument, Layer(priority = 6, 
									scale_up_button = self._touchpad[7], 
									scale_down_button = self._touchpad[6],
									offset_up_button = self._touchpad[5], 
									offset_down_button = self._touchpad[4],
									vertical_offset_up_button = self._touchpad[3],
									vertical_offset_down_button = self._touchpad[2],
									split_button = self._touchpad[0], 
									sequencer_button = self._touchpad[1]))
		self._instrument.drumpad_shift_layer = AddLayerMode(self._instrument, Layer(priority = 6, 
									scale_up_button = self._touchpad[7],
									scale_down_button = self._touchpad[6],
									drum_offset_up_button = self._touchpad[5], 
									drum_offset_down_button = self._touchpad[4],
									drumpad_mute_button = self._touchpad[3],
									drumpad_solo_button = self._touchpad[2],
									split_button = self._touchpad[0], 
									sequencer_button = self._touchpad[1]))
		self._instrument._keypad.main_layer = LayerMode(self._instrument._keypad, Layer(priority = 6, keypad_matrix = self._base_grid))
		self._instrument._keypad.sequencer_layer = LayerMode(self._instrument._keypad, Layer(priority = 6, playhead = self._playhead_element, keypad_matrix = self._base_grid.submatrix[:, 2:4], sequencer_matrix = self._base_grid.submatrix[:, :2]))
		self._instrument._keypad.split_layer = LayerMode(self._instrument._keypad, Layer(priority = 6, keypad_matrix = self._base_grid.submatrix[:, 2:4], split_matrix = self._base_grid.submatrix[:, :2]))
		self._instrument._keypad.sequencer_shift_layer = LayerMode(self._instrument._keypad, Layer(priority = 6, keypad_matrix = self._base_grid.submatrix[:, 2:4], loop_selector_matrix = self._base_grid.submatrix[:, :1], quantization_buttons = self._base_grid.submatrix[:7, 1:2], follow_button = self._pad[15]))
		self._instrument._drumpad.main_layer = LayerMode(self._instrument._drumpad, Layer(priority = 6, drumpad_matrix = self._base_grid))
		self._instrument._drumpad.sequencer_layer = LayerMode(self._instrument._drumpad, Layer(priority = 6, playhead = self._playhead_element, drumpad_matrix = self._base_grid.submatrix[:4, :], sequencer_matrix = self._base_grid.submatrix[4:8, :]))
		self._instrument._drumpad.split_layer = LayerMode(self._instrument._drumpad, Layer(priority = 6, drumpad_matrix = self._base_grid.submatrix[:4, :], split_matrix = self._base_grid.submatrix[4:8, :]))
		self._instrument._drumpad.sequencer_shift_layer = LayerMode(self._instrument._drumpad, Layer(priority = 6, drumpad_matrix = self._base_grid.submatrix[:4, :4], loop_selector_matrix = self._base_grid.submatrix[4:8, :2], quantization_buttons = quantgrid, follow_button = self._pad[31]))
		self._instrument._offset_component._on_value = 6
		self._instrument._scale_offset_component._on_value = 5
		self._instrument._drum_offset_component._on_value = 4
		self._instrument._split_mode_component._on_value = 1
		self._instrument._sequencer_mode_component._on_value = 3
		self._instrument.set_enabled(False)

		self._instrument._main_modes = ModesComponent(name = 'InstrumentModes')
		self._instrument._main_modes.add_mode('drumpad', [self._instrument._drumpad.main_layer, self.midi_mode_sysex])
		self._instrument._main_modes.add_mode('drumpad_split', [self._instrument._drumpad.split_layer, self.splitvertical_mode_sysex])
		self._instrument._main_modes.add_mode('drumpad_sequencer', [self._instrument._drumpad.sequencer_layer, self.splitvertical_mode_sysex])
		self._instrument._main_modes.add_mode('drumpad_shifted', [self._instrument.drumpad_shift_layer, self.midi_mode_sysex])
		self._instrument._main_modes.add_mode('drumpad_split_shifted', [self._instrument._drumpad.split_layer, self._instrument.drumpad_shift_layer])
		self._instrument._main_modes.add_mode('drumpad_sequencer_shifted', [self._instrument._drumpad.sequencer_shift_layer, self._instrument.drumpad_shift_layer, self.splitvertical_mode_sysex])
		self._instrument._main_modes.add_mode('keypad', [self._instrument._keypad.main_layer, self.midi_mode_sysex])
		self._instrument._main_modes.add_mode('keypad_split', [self._instrument._keypad.split_layer, self.splithorizontal_mode_sysex])
		self._instrument._main_modes.add_mode('keypad_sequencer', [self._instrument._keypad.sequencer_layer, self.splithorizontal_mode_sysex], )
		self._instrument._main_modes.add_mode('keypad_shifted', [self._instrument.keypad_shift_layer, self.midi_mode_sysex])
		self._instrument._main_modes.add_mode('keypad_split_shifted', [self._instrument._keypad.split_layer, self._instrument.keypad_shift_layer])
		self._instrument._main_modes.add_mode('keypad_sequencer_shifted', [self._instrument._keypad.sequencer_shift_layer, self._instrument.keypad_shift_layer, self.midi_mode_sysex])
		self._instrument._main_modes.add_mode('audioloop', [self._instrument.audioloop_layer, self.live_mode_sysex])
		#self._instrument._main_modes.add_mode('mod', [self._instrument.mod_layer])
		self._instrument.register_component(self._instrument._main_modes)
		self._instrument.set_enabled(False)
	

	def _setup_OSC_layer(self):
		self._OSC_id = 0
		if hasattr(__builtins__, 'control_surfaces') or (isinstance(__builtins__, dict) and 'control_surfaces' in __builtins__.keys()):
			for cs in __builtins__['control_surfaces']:
				if cs is self:
					break
				elif isinstance(cs, Base):
					self._OSC_id += 1

		self._prefix = '/Live/Base/'+str(self._OSC_id)
		self._outPrt = OSC_OUTPORT
		if not self.oscServer is None:
			self.oscServer.shutdown()
		self.oscServer = RemixNet.OSCServer('localhost', self._outPrt, 'localhost', 10001)
	

	def _setup_modswitcher(self):
		self._modswitcher = BaseDisplayingModesComponent(name = 'ModSwitcher')
		self._modswitcher.add_mode('mod', [self.modhandler], display_string = MODE_DATA['Mod'])
		self._modswitcher.add_mode('instrument', [self._instrument])
		#self._modswitcher.add_mode('disabled', [])
		self._modswitcher.selected_mode = 'instrument'
		self._modswitcher.set_enabled(False)
	

	def _setup_main_modes(self):
		self._main_modes = BaseDisplayingModesComponent(name = 'MainModes')
		self._main_modes.add_mode('Clips_shifted', [self._mixer.volume_layer, self._mixer.select_layer, self._mixer.channel_controls_layer, self.clips_layer_sysex, self.live_mode_sysex], groups = ['shifted'], behaviour = self._shift_latching(color = 8), display_string = MODE_DATA['Clips_shifted'])
		self._main_modes.add_mode('Clips', [self._mixer.volume_layer, self._mixer.select_layer, self._session.cliplaunch_layer,  self._session.navigation_layer, self.clips_layer_sysex, self.live_mode_sysex ], behaviour = self._shift_latching(color = 1), display_string = MODE_DATA['Clips'])
		self._main_modes.add_mode('Sends_shifted', [self.sends_layer_sysex, self._modswitcher, self._recorder.alt_layer, self._instrument.octave_toggle, tuple([self._send_instrument_shifted, self._send_instrument_unshifted]),], groups = ['shifted'], behaviour = self._shift_latching(color = 11), display_string = MODE_DATA['Sends_shifted'])
		self._main_modes.add_mode('Sends', [self.sends_layer_sysex, self._modswitcher, self._mixer.select_layer, self._mixer.selected_sends_layer, self._mixer.returns_layer,  self._transport.overdub_layer, self._recorder.main_layer,], behaviour = self._shift_latching(color = 4), display_string = MODE_DATA['Sends'])
		self._main_modes.add_mode('Device_shifted', [self.device_layer_sysex, self._modswitcher, tuple([self._send_instrument_shifted, self._send_instrument_unshifted]), self._device, self._device.parameters_layer, self._device_navigator.alt_layer,  ], groups = ['shifted'], behaviour = self._shift_latching(color = 10), display_string = MODE_DATA['Device_shifted'])
		self._main_modes.add_mode('Device', [self.device_layer_sysex, self._modswitcher, self._mixer.select_layer, self._mixer.select_layer, self._device, self._device.parameters_layer, self._device.nav_layer, self._device_navigator.main_layer,], behaviour = self._shift_latching(color = 3), display_string = MODE_DATA['Device'])
		self._main_modes.add_mode('User_shifted', [self._translations, self.user_layer_sysex, self.user_mode_sysex ], groups = ['shifted'], behaviour = self._shift_latching(color = 12), display_string = MODE_DATA['User_shifted'])
		self._main_modes.add_mode('User', [self._translations, self._mixer.select_layer, self.user_layer_sysex, self.user_mode_sysex], behaviour = self._shift_latching(color = 5), display_string = MODE_DATA['User'])
		self._main_modes.add_mode('Select', [self._mixer.select_layer, self._mixer.volume_layer, self._mixer.selected_channel_controls_layer, self._session.overlay_cliplaunch_layer, self._set_selected_channel_control_colors, self.clips_layer_sysex], behaviour = DelayedExcludingMomentaryBehaviour(excluded_groups = ['shifted']), display_string = MODE_DATA['Select'])
		self._main_modes.layer = Layer(priority = 4, Clips_button=self._button[0], Sends_button=self._button[1], Device_button=self._button[2], User_button=self._button[3], Select_button=self._touchpad_multi, display = self._display)
		self._main_modes.selected_mode = 'Clips'
	

	def _send_instrument_shifted(self):
		self._instrument.is_enabled() and self._instrument._on_shift_value(1)
		self.modhandler.is_enabled() and self.modhandler._shift_value(1)
	

	def _send_instrument_unshifted(self):
		self._instrument.is_enabled() and self._instrument._on_shift_value(0)
		self.modhandler.is_enabled() and self.modhandler._shift_value(0)
	

	def _set_selected_channel_control_colors(self):
		self._button[4].set_on_off_values(2, 0)
		self._button[5].set_on_off_values(3, 0)
		self._button[6].set_on_off_values(5, 0)
		self._button[7].set_on_off_values(7, 0)
		self._button[7].send_value(7, True)
	

	def _set_user_page_colors(self):
		self._button[4].set_on_off_values(1, 0)
		self._button[5].set_on_off_values(1, 0)
		self._button[6].set_on_off_values(1, 0)
		self._button[7].set_on_off_values(1, 0)
	

	def _notify_descriptors(self):
		if OSC_TRANSMIT:
			for pad in self._pad:
				self.oscServer.sendOSC(self._prefix+'/'+pad.name+'/lcd_name/', str(self.generate_strip_string(pad._descriptor)))
			for touchpad in self._touchpad:
				self.oscServer.sendOSC(self._prefix+'/'+touchpad.name+'/lcd_name/', str(self.generate_strip_string(touchpad._descriptor)))
			for button in self._button:
				self.oscServer.sendOSC(self._prefix+'/'+button.name+'/lcd_name/', str(self.generate_strip_string(button._descriptor)))
	

	def _get_devices(self, track):

		def dig(container_device):
			contained_devices = []
			if container_device.can_have_chains:
				for chain in container_device.chains:
					for chain_device in chain.devices:
						for item in dig(chain_device):
							contained_devices.append(item)
			else:
				contained_devices.append(container_device)
			return contained_devices
		

		devices = []
		for device in track.devices:
			for item in dig(device):
				devices.append(item)
				#self.log_message('appending ' + str(item))
		return devices
	

	def _register_pad_pressed(self, bytes):
		assert(len(bytes) is 8)
		#No damned bin() in Live.py math!!!???
		decoded = []
		for i in range(0, 8):
			bin = bytes[i]
			for index in range(0, 4):
				decoded.append(bin & 1)
				bin = bin>>1
		self._last_pad_stream = decoded
		for index in range(len(decoded)):
			self._stream_pads[index].press_flash(decoded[index])
	

	@subject_slot('value')
	def _on_nav_button_value(self, value, x, y, is_momentary):
		button = self._nav_buttons.get_button(x, y)
		if button in self._current_nav_buttons:
			if value > 0:
				self._send_midi((176, 35, DIRS[self._current_nav_buttons.index(button)]))
			else:
				self._display_mode()
	

	"""called on timer"""
	def update_display(self):
		super(Base, self).update_display()
		self._timer = (self._timer + 1) % 256
		self.flash()
	

	def flash(self):
		if(self.flash_status > 0):
			for control in self.controls:
				if isinstance(control, MonoButtonElement):
					control.flash(self._timer)
	

	"""m4l bridge"""
	def _on_device_name_changed(self):
		name = self._device.device_name_data_source().display_string()
		self._monobridge._send('Device_Name', 'lcd_name', str(self.generate_strip_string('Device')))
		self._monobridge._send('Device_Name', 'lcd_value', str(self.generate_strip_string(name)))
		self.touched()
		if OSC_TRANSMIT:
			self.oscServer.sendOSC(self._prefix+'/glob/device/', str(self.generate_strip_string(name)))
	

	def _on_device_bank_changed(self):
		name = 'No Bank'
		if is_device(self._device._device):
			name, _ = self._device._current_bank_details()
		self._monobridge._send('Device_Bank', 'lcd_name', str(self.generate_strip_string('Bank')))
		self._monobridge._send('Device_Bank', 'lcd_value', str(self.generate_strip_string(name)))
		self.touched()
	

	def _on_device_chain_changed(self):
		name = " "
		if is_device(self._device._device) and self._device._device.canonical_parent and isinstance(self._device._device.canonical_parent, Live.Chain.Chain):
			name = self._device._device.canonical_parent.name
		self._monobridge._send('Device_Chain', 'lcd_name', str(self.generate_strip_string('Chain')))
		self._monobridge._send('Device_Chain', 'lcd_value', str(self.generate_strip_string(name)))
		self.touched()
	

	def generate_strip_string(self, display_string):
		NUM_CHARS_PER_DISPLAY_STRIP = 12
		if (not display_string):
			return (' ' * NUM_CHARS_PER_DISPLAY_STRIP)
		else:
			display_string = str(display_string)
		if ((len(display_string.strip()) > (NUM_CHARS_PER_DISPLAY_STRIP - 1)) and (display_string.endswith('dB') and (display_string.find('.') != -1))):
			display_string = display_string[:-2]
		if (len(display_string) > (NUM_CHARS_PER_DISPLAY_STRIP - 1)):
			for um in [' ',
			 'i',
			 'o',
			 'u',
			 'e',
			 'a']:
				while ((len(display_string) > (NUM_CHARS_PER_DISPLAY_STRIP - 1)) and (display_string.rfind(um, 1) != -1)):
					um_pos = display_string.rfind(um, 1)
					display_string = (display_string[:um_pos] + display_string[(um_pos + 1):])
		else:
			display_string = display_string.center((NUM_CHARS_PER_DISPLAY_STRIP - 1))
		ret = u''
		for i in range((NUM_CHARS_PER_DISPLAY_STRIP - 1)):
			if ((ord(display_string[i]) > 127) or (ord(display_string[i]) < 0)):
				ret += ' '
			else:
				ret += display_string[i]

		ret += ' '
		ret = ret.replace(' ', '_')
		assert (len(ret) == NUM_CHARS_PER_DISPLAY_STRIP)
		return ret
	

	def notification_to_bridge(self, name, value, sender):
		#self.log_message('monobridge:' + str(name) + str(value))
		if isinstance(sender, MonoEncoderElement):
			if OSC_TRANSMIT:
				self.oscServer.sendOSC(self._prefix+'/'+sender.name+'/lcd_name/', str(self.generate_strip_string(name)))
				self.oscServer.sendOSC(self._prefix+'/'+sender.name+'/lcd_value/', str(self.generate_strip_string(value)))
			self._monobridge._send(sender.name, 'lcd_name', str(self.generate_strip_string(name)))
			self._monobridge._send(sender.name, 'lcd_value', str(self.generate_strip_string(value)))
		else:
			self._monobridge._send(name, 'lcd_name', str(self.generate_strip_string(name)))
			self._monobridge._send(name, 'lcd_value', str(self.generate_strip_string(value)))
			if OSC_TRANSMIT:
				self.oscServer.sendOSC(self._prefix+'/'+name+'/lcd_name/', str(self.generate_strip_string(name)))
				self.oscServer.sendOSC(self._prefix+'/'+name+'/lcd_value/', str(self.generate_strip_string(value)))
	

	def touched(self):
		if self._touched is 0:
			self._monobridge._send('touch', 'on')
			self.schedule_message(2, self.check_touch)
		self._touched +=1
	

	def check_touch(self):
		if self._touched > 5:
			self._touched = 5
		elif self._touched > 0:
			self._touched -= 1
		if self._touched is 0:
			self._monobridge._send('touch', 'off')
		else:
			self.schedule_message(2, self.check_touch)
		
	

	"""general functionality"""
	def disconnect(self):
		self._send_midi(STREAMINGOFF)
		if not self.oscServer is None:
			self.oscServer.shutdown()
		self.oscServer = None
		self.log_message("--------------= Base log closed =--------------")
		super(Base, self).disconnect()
		#rebuild_sys()
	

	def _can_auto_arm_track(self, track):
		routing = track.current_input_routing
		return routing == 'Ext: All Ins' or routing == 'All Ins' or routing.startswith('Base Input')
		#self._main_modes.selected_mode in ['Sends', 'Device'] and
	

	@subject_slot('appointed_device')
	def _on_device_changed(self):
		self.schedule_message(2, self._update_modswitcher)
		#pass
	

	def _on_selected_track_changed(self):
		super(Base, self)._on_selected_track_changed()
		self.schedule_message(1, self._update_modswitcher)
	

	def _update_modswitcher(self):
		debug('update modswitcher', self.modhandler.active_mod())
		if self.modhandler.active_mod():
			self._modswitcher.selected_mode = 'mod'
		else:
			self._modswitcher.selected_mode = 'instrument'
	

		"""if self._last_selected_track and self._last_selected_track.can_be_armed and not self._last_selected_track_arm:
			self.schedule_message(1, self._disarm_track, self._last_selected_track)
		if track.can_be_armed:
			self._last_selected_track_arm = track.arm
		if not self._last_selected_track is None and isinstance(self._last_selected_track, Live.Track.Track) and self._last_selected_track in track_list:
			if self._last_selected_track.current_input_sub_routing_has_listener(self._on_selected_track_midi_subrouting_changed):
				self._last_selected_track.remove_current_input_sub_routing_listener(self._on_selected_track_midi_subrouting_changed)
		self._last_selected_track = track"""

	

	def reset_controlled_track(self, track = None, *a):
		if not track:
			track = self.song().view.selected_track
		self.set_controlled_track(track)
	

	def set_controlled_track(self, track = None, *a):
		if isinstance(track, Live.Track.Track):
			super(Base, self).set_controlled_track(track)
		else:
			self.release_controlled_track()
	

	def restart_monomodular(self):
		#self.log_message('restart monomodular')
		self.modhandler.disconnect()
		with self.component_guard():
			self._setup_mod()
	

	def send_fader_color(self, num, value):
		self._send_midi((191, num+10, value))
	

	"""some cheap overrides"""
	def set_highlighting_session_component(self, session_component):
		self._highlighting_session_component = session_component
		if not session_component is None:
			self._highlighting_session_component.set_highlighting_callback(self._set_session_highlight)
	

	def handle_sysex(self, midi_bytes):
		#self.log_message('sysex: ' + str(midi_bytes))
		if len(midi_bytes) > 14:
			if midi_bytes[:6] == tuple([240, 0, 1, 97, 12, 64]):
				self._register_pad_pressed(midi_bytes[6:14])
			elif midi_bytes[3:10] == tuple([6, 2, 0, 1, 97, 1, 0]):
				if not self._connected:
					self._connected = True
					self._initialize_hardware()
	


#	a