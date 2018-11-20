#!/usr/bin/env python

from tkinter import *
import tkinter as tk 

from comtypes import *
import comtypes.client
from ctypes import POINTER
from ctypes.wintypes import DWORD, BOOL
import time 

from win10toast import ToastNotifier


###########################VARIABLES##################################

initVolume = 0




######################################################################



# credits - Himanshu dua @ Stackoverflow
MMDeviceApiLib = \
	GUID('{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
IID_IMMDevice = \
	GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
IID_IMMDeviceEnumerator = \
	GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
CLSID_MMDeviceEnumerator = \
	GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
IID_IMMDeviceCollection = \
	GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
IID_IAudioEndpointVolume = \
	GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')

class IMMDeviceCollection(IUnknown):
	_iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
	pass

class IAudioEndpointVolume(IUnknown):
	_iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
	_methods_ = [
		STDMETHOD(HRESULT, 'RegisterControlChangeNotify', []),
		STDMETHOD(HRESULT, 'UnregisterControlChangeNotify', []),
		STDMETHOD(HRESULT, 'GetChannelCount', []),
		COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
			(['in'], c_float, 'fLevelDB'),
			(['in'], POINTER(GUID), 'pguidEventContext')
		),
		COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
			(['in'], c_float, 'fLevelDB'),
			(['in'], POINTER(GUID), 'pguidEventContext')
		),
		COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
			(['out','retval'], POINTER(c_float), 'pfLevelDB')
		),
		COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
			(['out','retval'], POINTER(c_float), 'pfLevelDB')
		),
		COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
			(['in'], DWORD, 'nChannel'),
			(['in'], c_float, 'fLevelDB'),
			(['in'], POINTER(GUID), 'pguidEventContext')
		),
		COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
			(['in'], DWORD, 'nChannel'),
			(['in'], c_float, 'fLevelDB'),
			(['in'], POINTER(GUID), 'pguidEventContext')
		),
		COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
			(['in'], DWORD, 'nChannel'),
			(['out','retval'], POINTER(c_float), 'pfLevelDB')
		),
		COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
			(['in'], DWORD, 'nChannel'),
			(['out','retval'], POINTER(c_float), 'pfLevelDB')
		),
		COMMETHOD([], HRESULT, 'SetMute',
			(['in'], BOOL, 'bMute'),
			(['in'], POINTER(GUID), 'pguidEventContext')
		),
		COMMETHOD([], HRESULT, 'GetMute',
			(['out','retval'], POINTER(BOOL), 'pbMute')
		),
		COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
			(['out','retval'], POINTER(c_float), 'pnStep'),
			(['out','retval'], POINTER(c_float), 'pnStepCount'),
		),
		COMMETHOD([], HRESULT, 'VolumeStepUp',
			(['in'], POINTER(GUID), 'pguidEventContext')
		),
		COMMETHOD([], HRESULT, 'VolumeStepDown',
			(['in'], POINTER(GUID), 'pguidEventContext')
		),
		COMMETHOD([], HRESULT, 'QueryHardwareSupport',
			(['out','retval'], POINTER(DWORD), 'pdwHardwareSupportMask')
		),
		COMMETHOD([], HRESULT, 'GetVolumeRange',
			(['out','retval'], POINTER(c_float), 'pfMin'),
			(['out','retval'], POINTER(c_float), 'pfMax'),
			(['out','retval'], POINTER(c_float), 'pfIncr')
		),

	]

class IMMDevice(IUnknown):
	_iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
	_methods_ = [
		COMMETHOD([], HRESULT, 'Activate',
			(['in'], POINTER(GUID), 'iid'),
			(['in'], DWORD, 'dwClsCtx'),
			(['in'], POINTER(DWORD), 'pActivationParans'),
			(['out','retval'], POINTER(POINTER(IAudioEndpointVolume)), 'ppInterface')
		),
		STDMETHOD(HRESULT, 'OpenPropertyStore', []),
		STDMETHOD(HRESULT, 'GetId', []),
		STDMETHOD(HRESULT, 'GetState', [])
	]
	pass

class IMMDeviceEnumerator(comtypes.IUnknown):
	_iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')

	_methods_ = [
		COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
			(['in'], DWORD, 'dataFlow'),
			(['in'], DWORD, 'dwStateMask'),
			(['out','retval'], POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')
		),
		COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
			(['in'], DWORD, 'dataFlow'),
			(['in'], DWORD, 'role'),
			(['out','retval'], POINTER(POINTER(IMMDevice)), 'ppDevices')
		)
	]





enumerator = comtypes.CoCreateInstance( 
	CLSID_MMDeviceEnumerator,
	IMMDeviceEnumerator,
	comtypes.CLSCTX_INPROC_SERVER
)


toaster = ToastNotifier()


def minimizeToTray():
	master.wm_state('iconic')


def start_bivalues():

	toaster.show_toast("BALSA","is now running")

	delay_time = delay_slider.get()
	reps = rep_slider.get()
	
	# print enumerator
	endpoint = enumerator.GetDefaultAudioEndpoint( 0, 1 )
	# print endpoint
	volume = endpoint.Activate( IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )
	initVolume = volume.GetMasterVolumeLevel()
	#print volume
	#print volume.GetMasterVolumeLevel()
	# print volume.GetVolumeRange()
	#volume.SetMasterVolumeLevel(-65, None) uncomment for 0 volume
	#volume.SetMasterVolumeLevel(-1, None) uncomment for full volume
	#volume.SetMasterVolumeLevel(-25, None) #Change the first argument for controlling the volume remember it should be -ve not less than -65

	for x in xrange(0, reps):

		if (smooth_box.get()) == 0:

			volume.SetChannelVolumeLevel(0,initVolume,None)
			volume.SetChannelVolumeLevel(1,-65,None)

			time.sleep(delay_time) 
			print("Changed")

			volume.SetChannelVolumeLevel(0,-65,None)
			volume.SetChannelVolumeLevel(1,initVolume,None)


			time.sleep(delay_time) 
			print("Rep Done")

		elif (smooth_box.get()) == 1:

			stepIncrement = 5
			

			ch0_volume = -18
			ch1_volume = -65

			while (ch0_volume != -65 and ch1_volume != -18):

				volume.SetChannelVolumeLevel(0,ch0_volume,None)
				volume.SetChannelVolumeLevel(1,ch1_volume,None)

				ch0_volume = ch0_volume - stepIncrement
				ch1_volume = ch1_volume + stepIncrement

				if ch0_volume <= -65:
					ch0_volume = -65
				if ch1_volume >= -18:
					ch1_volume = -18

				time.sleep(0.08)

			ch0_volume = -65
			ch1_volume = -18

			time.sleep(1)


			while (ch1_volume != -65 and ch0_volume != -18):

				volume.SetChannelVolumeLevel(0,ch0_volume,None)
				volume.SetChannelVolumeLevel(1,ch1_volume,None)

				ch0_volume = ch0_volume + stepIncrement
				ch1_volume = ch1_volume - stepIncrement

				if ch1_volume <= -65:
					ch1_volume = -65
				if ch0_volume >= -18:
					ch0_volume = -18

				time.sleep(0.08)

			time.sleep(1)

	volume.SetChannelVolumeLevel(0,initVolume,None)
	volume.SetChannelVolumeLevel(1,initVolume,None)
  
	print("Done")

# credits - Adam Luchjenbroers, stackoverflow
def translate(value, leftMin, leftMax, rightMin, rightMax):
	# Figure out how 'wide' each range is
	leftSpan = leftMax - leftMin
	rightSpan = rightMax - rightMin

	# Convert the left range into a 0-1 range (float)
	valueScaled = float(value - leftMin) / float(leftSpan)

	# Convert the 0-1 range into a value in the right range.
	return rightMin + (valueScaled * rightSpan)

# convert user input value(0 to 100) into machine values (0 to -65)
# def volume_converter:

if __name__ == "__main__":

	master = Tk()

	button_frame = tk.Frame(master)
	button_frame.pack(fill=tk.X, side=tk.BOTTOM)

	delay_slider = Scale(master, from_=0, to=10, resolution=1, tickinterval=1, length=400, orient=HORIZONTAL)
	delay_slider.pack()
	delay_slider.set(3)

	rep_slider = Scale(master, from_=0, to=10, resolution=1, tickinterval=1, length=400, orient=HORIZONTAL)
	rep_slider.pack()
	rep_slider.set(3)

	smooth_box = IntVar()
	Checkbutton(master, text="Smooth", variable=smooth_box).pack()

	start_button = Button(button_frame, text='Start', command=start_bivalues)
	pause_button = Button(button_frame, text='Pause', command=minimizeToTray)
	#cycle_button = Button(button_frame, text='Cycle', command=)

	button_frame.columnconfigure(0, weight=1)
	button_frame.columnconfigure(1, weight=1)

	start_button.grid(row=0, column=1, sticky=tk.W+tk.E)
	pause_button.grid(row=0, column=0, sticky=tk.W+tk.E)

	mainloop()