import numpy
import ctypes
import traceback
from ctypes import *
from ctypes.wintypes import *
import time
import struct
from pylab import *
import astropy.io.fits as pyfits
from multiprocessing import Queue, Lock
from threading import Thread
import datetime
import os
import settings
import analyze_data
import sys
import traceback


from numpy import *
AT_HANDLE_SYSTEM = 1
AT_SUCCESS = 0


class Zyla_Camera(object):
    def __init__(self):
        self._dataDirectory = "D:\\Aeroforecast_Data\\"
       
        self._width = 600
        self._height = 600
        self._left = 730
        self._top = 680
        self._frames = 100
        
        self._image = numpy.zeros((self._width,self._height))
        
        self._lock = Lock()
        self._open = False
        self.lib = ctypes.windll.LoadLibrary("atcore.dll");
        self.lib_utility = ctypes.windll.LoadLibrary("atutility.dll");
        self.lib_utility.AT_InitialiseUtilityLibrary();
        self.lib.AT_InitialiseLibrary();
        self.lib.AT_SetEnumeratedString.argtypes = [c_int,c_wchar_p,c_wchar_p]
        self.lib.AT_SetFloat.argtypes = [c_int,c_wchar_p,c_double]
        self.lib.AT_GetInt.argtypes = [c_int,c_wchar_p, POINTER(c_long)]
        self.lib.AT_WaitBuffer.argtypes = [c_int,POINTER(POINTER(c_ubyte)),POINTER(c_int),c_int]
        
        self.vs = [0]
        self.Ps = [0]
        self.Ts = [0]
        
        self.data_queue = Queue()
        self.background_thread = Thread(target = self.save_thread,args=(self.data_queue,))
        self.background_thread.daemon = True
        self.background_thread.start()
        
        self._run = False
        self._allow_save = False
        self.bkg_thread = Thread(target=self.update,args=())
        self.bkg_thread.daemon = True
        self.bkg_thread.start()
        
        device_count = self.get_int("Device Count")
        print("{} devices found.".format(device_count.value))
    
    @property
    def wind_data(self):
        return self.vs,self.Ps,self.Ts
    
    
    def save(self):
        try:
            fitsData = zeros(self._width*self._height*self._frames,dtype=np.uint16)
            fitsData = fitsData.reshape(self._frames,self._width,self._height)
            index=0
            
            for data in dataSet:
                data = self._deviceManager.camera.getData()
                print("Min Value: {}".format(min(data)))
                fitsData[index] = data
                index+=1
            hdu = pyfits.PrimaryHDU(fitsData)
            hdulist = pyfits.HDUList([hdu])

            utc_datetime = datetime.datetime.utcnow()
            epoch = datetime.datetime.utcfromtimestamp(0)
            txt = utc_datetime.strftime("%Y-%m-%d_%H%M%S_%f")
            seconds = (utc_datetime-epoch).total_seconds()
            print("Data Saved to {}\\Camera\\{}_{:2.3f}.fits".format(self._currentSyncDataDir,txt,seconds))
            hdulist.writeto("{}\\Camera\\{}_{:2.3f}.fits".format(self._currentSyncDataDir,txt,seconds));
        except:
            traceback.print_exc(file=sys.stdout)
            print("Error Saving out dataset")
    
        
    def get_int(self,setting_name):
        hndl = AT_HANDLE_SYSTEM
        if self._open:
            hndl = self._hndl
        int_val = c_long(0)    
        self.lib.AT_GetInt.argtypes = [c_int,c_wchar_p, POINTER(c_long)]
        char_val = c_wchar_p(setting_name)
        ret = self.lib.AT_GetInt(hndl, char_val, int_val)
        if ret != 0:
            print("Error getting int value: {}".format(ret))
            traceback.print_exc(file=sys.stdout)
        return int_val
        
    def set_enum(self,name,value):
        if self._open:
            ret = self.lib.AT_SetEnumeratedString(self._hndl.value,c_wchar_p(name),c_wchar_p(value))
            if ret!=AT_SUCCESS:
                print("Error setting Enum Value: {} ({})".format(name,ret))

    def set_float(self,name,value):
        if self._open:
            ret = self.lib.AT_SetFloat(self._hndl, c_wchar_p(name), value);
            if ret !=  AT_SUCCESS:
                print("Error setting float Value: {} ({})".format(name,ret ))
                
    def set_int(self,name,value):
        if self._open:
            ret = self.lib.AT_SetInt(self._hndl, c_wchar_p(name), value);
            if ret !=  AT_SUCCESS:
                print("Error setting int Value: {} ({})".format(name,ret ))
            
    def open(self):
        try:
            self._hndl = c_int(0)
            self.lib.AT_Open.argtypes = [c_int,POINTER(c_int)]
            ret = self.lib.AT_Open(0, self._hndl);
            if ret == AT_SUCCESS:
                self._open = True
                self.init()
                self._run = True
                analyze_data.start()
                self.command("Acquisition Start");
        except:
            self._open = False
            print("Error Opening Andor Zyla Camera")
            traceback.print_exc(file=sys.stdout)
            
    def init(self):
        if self._open:
            self.set_enum("Pixel Encoding","Mono16")
            
            self.set_float("Exposure Time", settings.exposure)
            self.set_enum("SimplePreAmpGainControl","16-bit (low noise & high well capacity)")
            self.set_enum("CycleMode","Continuous")
            
            self.set_enum("AOIBinning","1x1")
            
            self.set_int("AOIWidth",self._width)
            self.set_int("AOIHeight",self._height)
            
            self.set_int("AOILeft",self._left)
            self.set_int("AOITop",self._top)
            
            self.set_enum("Pixel Readout Rate","280 MHz")
            
            self._image_size = self.get_int("Image Size Bytes");
            print("Image Size: {}".format(self._image_size.value))
            self._userBuffer = (c_ubyte*self._image_size.value)()
            self.queue_buffer()
            
            
            self._image_buffer = []
            for idx in range(0,self._frames):
                self._image_buffer.append(POINTER(c_ubyte)())

    @property
    def ready(self):
        return self._open
    
    def queue_buffer(self):
        if self._open:
            ret = self.lib.AT_QueueBuffer(self._hndl,self._userBuffer,self._image_size)
            if ret!=AT_SUCCESS:
                print("Queue Buffer: {}".format(ret))
    
    
    def command(self,command):
        if self._open:
            ret = self.lib.AT_Command(self._hndl, c_wchar_p(command));
            if ret != AT_SUCCESS:
                print("Error sending Command {}: {}".format(command,ret))
    
    def start(self,data_directory=None):
        with self._lock:
            if data_directory is not None:
                self._currentSyncDataDir = data_directory
            else:
                self.createNewDirectory()
            
            self._allow_save = True
        
    def stop(self):
        with self._lock:
            self._allow_save = False
            

    def snap(self):
        with self._lock:
            if self._run:
                start = time.time()
                bufferSize = (self._width*self._height)*ctypes.sizeof(ctypes.c_short)           
                rgb_buffer = ctypes.create_string_buffer(bufferSize)
                for idx in range(0,self._frames):
                    if not self._open or not self._run:
                        break
                    ret = self.lib.AT_WaitBuffer(self._hndl, byref(self._image_buffer[idx]),  self._image_size, 10000)
                    if ret != AT_SUCCESS:
                        print("WaitBuffer returned: {}".format(ret))
                        
                   
                    utc_datetime = datetime.datetime.utcnow()
                    epoch = datetime.datetime.utcfromtimestamp(0)
                    seconds = (utc_datetime-epoch).total_seconds()
                    
                    self.data_queue.put((seconds,idx))
                    if self._open and self._run:
                        ret = self.lib.AT_QueueBuffer(self._hndl,self._userBuffer,self._image_size)
                        if ret != AT_SUCCESS:
                            print("QueueBuffer returned: {}".format(ret))
                end = time.time();
        
    def close(self):
        if self._open:
            self._run = False
            self._open = False
            self.command("Acquisition Stop");
            self.lib.AT_Close(self._hndl.value);

    def update(self):
        while True:
            while self._run:
                self.snap()
            time.sleep(1)

    @property
    def image(self):
        return self._image
    
    def save_thread(self,queue):
        data_index=0
        fitsData = zeros(self._width*self._height*20,dtype=np.uint16)
        fitsData = fitsData.reshape(20,self._width,self._height)
        
        bufferSize = (self._width*self._height)*ctypes.sizeof(ctypes.c_ushort)           
        rgb_buffer = ctypes.create_string_buffer(bufferSize)
        
        while True:
            try:
                time_stamp, buffer_index = queue.get()
                if queue.qsize()>=100:
                    print("Queue Size: {} at {}".format(queue.qsize(), time_stamp))
                    
                ctypes.memmove(rgb_buffer, self._image_buffer[buffer_index], bufferSize)
                data = numpy.array(struct.unpack("{0}H".format(self._width*self._height),rgb_buffer))
                data = data.reshape(self._width,self._height);
                self._image = data
                
                
                
                if not self._allow_save:
                    continue
                    
                   
                fitsData[data_index] = data
                data_index += 1
                if data_index == 20:
                    data_index=0
                    seconds = time.time()
                    
                    utc_datetime = datetime.datetime.utcnow()
                    epoch = datetime.datetime.utcfromtimestamp(0)
                    txt = utc_datetime.strftime("%Y-%m-%d_%H%M%S_%f")
                    seconds = (utc_datetime-epoch).total_seconds()
                    hdu = pyfits.PrimaryHDU(fitsData)
                    
                    hdulist = pyfits.HDUList([hdu])
                    hdulist.writeto("{}\\Camera\\{:2.3f}.fits".format(self._currentSyncDataDir,time_stamp));
                
            except:
                traceback.print_exc(file=sys.stdout)
            
    def createNewDirectory(self):
        folderName = ""
        utc_datetime = datetime.datetime.utcnow()
        txt = utc_datetime.strftime("%Y%m%d%H%M%S")
        
        if len(folderName)>0:
            self._currentDataDir = "{0}{1}_{2}".format(self._dataDirectory, txt,folderName)
            self._currentSyncDataDir = "{0}{1}_{2}/Sync_Data".format(self._dataDirectory, txt,folderName)
            self._currentNonSyncDataDir = "{0}{1}_{2}/Non_Sync_Data".format(self._dataDirectory, txt,folderName)
        else:
            self._currentDataDir = "{0}{1}".format(self._dataDirectory, txt)
            self._currentSyncDataDir = "{0}{1}/Sync_Data".format(self._dataDirectory, txt)
            self._currentNonSyncDataDir = "{0}{1}/Non_Sync_Data".format(self._dataDirectory, txt)
        
        os.mkdir(self._currentDataDir);
        os.mkdir(self._currentSyncDataDir);
        os.mkdir(self._currentNonSyncDataDir);

        cameraPath = "{0}/{1}".format(self._currentSyncDataDir,"Camera")
        os.mkdir(cameraPath);
        

     
if __name__ == "__main__":
   
    camera = Zyla_Camera()
    camera.open()
    camera.start()
    s = time.time()
    time.sleep(10)
    for idx in range(0,10):
        camera.snap()
    e = time.time()
    print("*"*79)
    print("Total Time: {}".format(e-s))
    print("*"*79)
    
    camera.stop()
    camera.close()
    
    
