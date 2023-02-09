import ctypes as c                # import the C compatible data types
from sys import platform, path    # this is needed to check the OS type and get the PATH
from os import sep                # OS specific file path separators
import numpy as np


# import waveforms parameters and the C library
if platform.startswith("win"):
    # on Windows
    dwf = c.cdll.dwf
    constants_path = "C:" + sep + "Program Files (x86)" + sep + "Digilent" + sep + "WaveFormsSDK" + sep + "samples" + sep + "py"
elif platform.startswith("darwin"):
    # on macOS
    lib_path = sep + "Library" + sep + "Frameworks" + sep + "dwf.framework" + sep + "dwf"
    dwf = c.cdll.LoadLibrary(lib_path)
    constants_path = sep + "Applications" + sep + "WaveForms.app" + sep + "Contents" + sep + "Resources" + sep + "SDK" + sep + "samples" + sep + "py"
else:
    # on Linux
    dwf = c.cdll.LoadLibrary("libdwf.so")
    constants_path = sep + "usr" + sep + "share" + sep + "digilent" + sep + "waveforms" + sep + "samples" + sep + "py"

path.append(constants_path)

import dwfconstants as dwfc


# Basic IO
def connect(number=0):
    hdwf = c.c_int()

    # Check for available devices
    cdevices = c.c_int()
    dwf.FDwfEnum(c.c_int(0), c.byref(cdevices))
    if cdevices.value == 0:
        raise Exception("No device connected")

    # Connect to device and get handle as hdwf
    dwf.FDwfDeviceOpen(c.c_int(number), c.byref(hdwf))
    if hdwf.value == dwfc.hdwfNone.value:
        raise Exception("Failed to connect to device")
    
    return hdwf


def disconnect():
    dwf.FDwfDeviceCloseAll()


# Configuring Wavegen channels 0, 1
def config_wavegen(
    hdwf,
    # wavegen settings
    frequency,                              # max 10 MHz
    amplitude,                              # max 5 V
    signal_shape = dwfc.funcSine,           # output signal shape: funcSine, funcSquare, funcTriangle, funcRampUp, funcRampDown, funcNoise
    offset = 0,                             # signal voltage offset
    phase = 0,                              # signal phase
    symmetry = 50,                          # signal symmetry shape
    channel = 0                             # channel 0 / 1 (or -1 for all channels) 
    ):

    channel = c.c_int(channel)

    dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, dwfc.AnalogOutNodeCarrier, c.c_bool(True))
    dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, dwfc.AnalogOutNodeCarrier, signal_shape)
    dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, dwfc.AnalogOutNodeCarrier, c.c_double(frequency))
    dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, dwfc.AnalogOutNodeCarrier, c.c_double(amplitude))
    dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, dwfc.AnalogOutNodeCarrier, c.c_double(offset))
    dwf.FDwfAnalogOutNodePhaseSet(hdwf, channel, dwfc.AnalogOutNodeCarrier, c.c_double(phase))
    dwf.FDwfAnalogOutNodeSymmetrySet(hdwf, channel, dwfc.AnalogOutNodeCarrier, c.c_double(symmetry))


def start_wavegen(hdwf, channel):
    channel = c.c_int(channel)
    dwf.FDwfAnalogOutConfigure(hdwf, channel, c.c_int(1))


def stop_wavegen(hdwf, channel):
    channel = c.c_int(channel)
    dwf.FDwfAnalogOutConfigure(hdwf, channel, c.c_int(0))


def reset_wavegen(hdwf, channel=c.c_int(-1)):
    channel = c.c_int(channel)
    dwf.FDwfAnalogOutReset(hdwf, channel)


# Configuring Oscilloscope channels 0, 1
def config_oscilloscope(
    hdwf,
    # oscilloscope settings
    range0,                     # Oscilloscope Channel 1 voltage range, max 25 V
    range1,                     # Oscilloscope Channel 2
    sample_rate,                # max 100 MHz
    sample_size = 8192,         # max 8192, sample time = sample_size / sample_rate
    ):

    # configure oscilloscope
    sample_rate = 100e6 if sample_rate >= 100e6 else sample_rate
    dwf.FDwfAnalogInFrequencySet(hdwf, c.c_double(sample_rate))             # set sampling rate
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c.c_int(0), c.c_double(range0))   # set channel 0 range
    dwf.FDwfAnalogInChannelRangeSet(hdwf, c.c_int(1), c.c_double(range1))   # set channel 1 range
    dwf.FDwfAnalogInBufferSizeSet(hdwf, c.c_int(sample_size))               # set sample size


def measure_oscilloscope(hdwf):
    sample_rate = c.c_double()
    dwf.FDwfAnalogInFrequencyGet(hdwf, c.byref(sample_rate))
    sample_size = c.c_int()
    dwf.FDwfAnalogInBufferSizeGet(hdwf, c.byref(sample_size))
    sample_size = sample_size.value

    # start oscilloscope
    dwf.FDwfAnalogInConfigure(hdwf, c.c_int(1), c.c_bool(True))

    # run until buffer is filled
    status = c.c_int()
    while not status.value == dwfc.DwfStateDone.value:
        dwf.FDwfAnalogInStatus(hdwf, c.c_int(1), c.byref(status))
    
    # get data as python variables
    t = np.arange(sample_size) / sample_rate.value                # time data

    rg0 = (c.c_double*sample_size)()                                      # get channel 1 data
    dwf.FDwfAnalogInStatusData(hdwf, c.c_int(0), rg0, sample_size)
    v0 = np.fromiter(rg0, dtype=float)

    rg1 = (c.c_double*sample_size)()                                      # get channel 2 data
    dwf.FDwfAnalogInStatusData(hdwf, c.c_int(1), rg1, sample_size)
    v1 = np.fromiter(rg1, dtype=float)

    return t, v0, v1
