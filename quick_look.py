from time import time, sleep
import numpy as np
import pylab as plt
import serial
import re
from glob import glob
from scipy.signal import resample
import scipy
#from filters import lowpass
import seaborn # makes plots look nicer: pip install seaborn at the term.
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

def find_serial_devices():
    '''Find serial devices connected to the computer.'''

    # Define the REGEX for finding a serial port!
    SERIAL_REGEX = r"/dev/tty.usbmodem"

    # Grab list of devices.
    devices = glob('/dev/*')
    valid_devices = []
    for device in devices:
        if re.search(SERIAL_REGEX, device):
            valid_devices.append(device)
    return valid_devices


def collect_data(serial_port_id, duration, commands=[], baud_rate=9600,\
        verbose=False):
    '''Collect data from a BioMonitor device on the specified serial port.
    INPUTS
        serial_port_id - string
            The name of the serial port you would like to connect to. Typically
            looks something like '/dev/tty.usbserial-FT9J9DNE'.
        duration - float
            The requested collection time, in seconds.
        commands - array_like
            A list of string commands to send to the BioMonitor before reading
            data. For example, commands=['R', 's 21 01'] will send the reset
            command, followed by a sampling rate change command. Data reading
            from the serial port will start after the commands are issued.
        verbose - array_like
            If set to True, The first 10 serial commands will be printed to the
            screen. This is useful for debugging, or for ensuring that commands
            are being recognized.
    OUTPUTS
        channels_available - array_like
            A list of channels present in the data collection. For example, if
            channels 0 and 5 are active, channels_available = [0, 5]. These
            channel numbers are used as keys to access the contents of the
            dictionaries.
        timestamps - dict
            A dictionary of timestamps. The keys to the dictionary correspond
            to the channel numbers. For example, timestamps[0] returns an array
            of timestamps associated with channel 0. Timestamps are 24-bit
            integers; units are milliseconds.
        values - dict
            A dictionary of values. The keys to the dictionary corresponds to
            the channel numbers. For example, values[5] returns an array of
            voltage values collected from channel 5. Units are floats in volts,
            and are between 0.0 and 3.3 volts.
    '''

    # 24-bit MAXVAL constant for scaling voltage output.
    MAXVAL = 2**24-1
    MAXREF = 2.5
    COVFAC = MAXREF*(1/MAXVAL)
    # Open the serial port in a with block.
    with serial.Serial(serial_port_id, baud_rate) as ser:

        # First write requested commands.
        for command in commands:
            pass
            # ser.write(bytes(command.encode()))

        if verbose:
            # Print data to screen, if you want.
            for itr in range(10):
                print(ser.readline())

        timestamps = {}
        values = {}
        for k in [0,1,2]:
            values[k] = []
            timestamps[k] = []
        start_time = time()
        biomonitor_regex = r"(B1)\s*(\d*)\s*(\w{0,8})\s*(\w*)"

        channels_available = set()
        while ((time() - start_time) < duration):
            biomonitor_output = ser.readline()
            out = re.search(biomonitor_regex, str(biomonitor_output))
            # print(biomonitor_output)
            if out:
                # We caught something!
                if out.group(1) == 'B1':
                    # Looks like we have some BioMonitor output.
                    try: # channel number there?
                        channel_number = int(out.group(2), 16)
                        channels_available.add(channel_number)
                    except:
                        pass
                    try: # voltage value present?
                        values[channel_number].append(int(out.group(3),16))
                    except:
                        pass
                    try: # timestamp present?
                        timestamps[channel_number].append(int(out.group(4),16))
#                        print(int(out.group(4),16))
                    except:
                        pass

    # Convert the timestamps and values into numpy arrays -- easier!
    for chn in channels_available:
        try: # were timestamps present?
            timestamps[chn] = np.vstack(timestamps[chn])
            timestamps[chn] -= timestamps[chn][0]
        except:
            pass
        try: # were voltage values reported?
            values[chn] = np.vstack(values[chn])*COVFAC
#            values[chn] = np.vstack(values[chn])/MAXVAL*2.5
        except:
            pass

    # We're done here. Peace!
    return list(channels_available), timestamps, values


if __name__ =='__main__':

    # CHANGE THIS TO YOUR LOCAL SERIAL PORT!!!!!
    connect_id = '/dev/tty.Bluetooth-Incoming-Port'

    commands = []
    duration = 10 # seconds

    # Collect the data.
    chans, ts, vals = collect_data(connect_id, duration, commands, verbose=0)

    # Plot the data. By default, the code below will plot data from all the
    # channels. If you only want to plot data from a subset of the channels,
    # specify chans = [0,1], for example, to only plot channels 0 and 1.

    # Specify the subset of channels whose data you wish to plot.
    chans = [0]

    plt.ion()
    plt.close('all')
    plt.figure('Latest Data')
    for chn in chans:
        y = vals[chn].flatten()
        t = ts[chn].flatten()

        fs = 1/np.median(np.diff(t)*1e-6)

        # Build a low pass filter.
        # nyquist=0.5*fs
        # f_low = 10/nyquist
        # a,b  = scipy.signal.butter(5, f_low, 'low', analog=False)
        # y_filt = scipy.signal.lfilter(a, b, y, axis=-1, zi=None)
        y_filt, _ = y,_#lowpass(1e-6*t, y, freq_cutoff=10, filter_order=5)

        label='Channel {:d}'.format(chn)

        # Otherwise, we just plot the channel data.
        plt.plot(t*1e-6, y_filt, linewidth=1, label=label)

        # Make the plot more useful.
        plt.grid(True)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Voltage')
        plt.legend()

