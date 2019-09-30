# AIM XRK Wrapper Class
# Brian Acosta 
# May 16th, 2018
#
#
# Distributed under creative commons beerware license:
# Free, but if you use it and we ever meet you buy me a beer.   
# 

from ctypes import *
import os 
from xrk_util import *

class XRK():
    def __init__(self, filename):
        
        self.filename = filename
        self.fileptr = file_pointer(self.filename)
        self.idxf = aimXRK.open_file(self.fileptr.value)
        self.channels = self.channel_list()
        self.GPS_channels = self.GPS_channel_list()
        self.GPS_raw_channels = self.GPS_raw_channel_list()
        
        if not self.idxf > 0:
            del self 
           
    def close(self):
        success = aimXRK.close_file_i(self.idxf)
        return (success > 0)
    
    # returns a string of the vehicle name
    def vehicle_name(self):
        return c_char2Str(c_char_p(aimXRK.get_vehicle_name(self.idxf)))
    
    # returns a string of the track name   
    def track_name(self):
        return c_char2Str(c_char_p(aimXRK.get_track_name(self.idxf)))
    
    # returns a string of the racer's name
    def racer_name(self):
        return c_char2Str(c_char_p(aimXRK.get_racer_name(self.idxf)))
    
    # returns a string of the championship name
    def championship_name(self):
        return c_char2Str(c_char_p(aimXRK.get_championship_name(self.idxf)))
    
    # returns a string of the venue type
    def venue_type(self):
        return c_char2Str(c_char_p(aimXRK.get_venue_type_name(self.idxf)))
    
    # returns an integer lap count
    def lap_count(self):
        return aimXRK.get_laps_count(self.idxf)
    
    # returns a list of the lap times in the given run
    def lap_times_list(self):
        laps = self.lap_count()
        current_start = c_double(0)
        current_duration = c_double(0)
        
        lap_starts = []
        lap_times = []
        
        for i in range(laps):
            aimXRK.get_lap_info(self.idxf, i, byref(current_start), byref(current_duration))
            lap_starts.append(current_start.value)
            lap_times.append(current_duration.value)
            
        return lap_times
        
    ############################################################################
    ## REGULAR DATA CHANNEL MEHTODS
    ############################################################################
        
    def channel_count(self):
        return aimXRK.get_channels_count(self.idxf)
             
    def channel_list(self):
        channel_names = []
        
        for i in range(self.channel_count()):
            channel_i = c_char2Str(c_char_p(aimXRK.get_channel_name(self.idxf, i)))
            channel_names.append(channel_i) 
        
        return channel_names
        
    def channel_sample_count(self, channel_name):
        try:
            idxc = self.channels.index(channel_name)
            return aimXRK.get_channel_samples_count(self.idxf, idxc)
        except:
            return 0

    def channel_sample_count_by_index(self, idxc):
        return aimXRK.get_channel_samples_count(self.idxf, idxc)
    
    def channel_units(self, channel_name):
        try:
            idxc = self.channels.index(channel_name)
            return c_char2Str(c_char_p(aimXRK.get_channel_units(self.idxf, idxc)))
        except:
            return 0
            
    def channel_units_by_index(self, idxc):
        return c_char2Str(c_char_p(aimXRK.get_channel_units(self.idxf, idxc)))
        
    def channel_times_and_samples(self, channel_name):
        idxc = self.channels.index(channel_name)
        sample_count = self.channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_channel_samples(self.idxf, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def channel_times_and_samples_by_index(self, idxc):
        sample_count = self.channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_channel_samples(self.idxf, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def lap_channel_sample_count(self, channel_name, lap_number):
        idxl = lap_number - 1 
        try:
            idxc = self.channels.index(channel_name)
            return aimXRK.get_lap_channel_samples_count(self.idxf, idxl, idxc)
        except:
            return 0
            
    def lap_channel_sample_count_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        return aimXRK.get_lap_channel_samples_count(self.idxf, idxl, idxc)
        
    def lap_channel_times_and_samples(self, channel_name, lap_number):
        idxc = self.channels.index(channel_name)
        idxl = lap_number - 1
        sample_count = self.lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_lap_channel_samples(self.idxf, idxl, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def lap_channel_times_and_samples_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        sample_count = self.lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_lap_channel_samples(self.idxf, idxl, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    ############################################################################
    ## GPS DATA CHANNEL MEHTODS
    ############################################################################  
  
    def GPS_channel_count(self):
        return aimXRK.get_GPS_channels_count(self.idxf)
        
    def GPS_channel_list(self):
        channel_names = []
        
        for i in range(self.GPS_channel_count()):
            channel_i = c_char2Str(c_char_p(aimXRK.get_GPS_channel_name(self.idxf, i)))
            channel_names.append(channel_i) 
        
        return channel_names
     
    def GPS_channel_sample_count(self, channel_name):
        try:
            idxc = self.GPS_channels.index(channel_name)
            return aimXRK.get_GPS_channel_samples_count(self.idxf, idxc)
        except:
            return 0

    def GPS_channel_sample_count_by_index(self, idxc):
        return aimXRK.get_GPS_channel_samples_count(self.idxf, idxc)
    
    def GPS_channel_units(self, channel_name):
        try:
            idxc = self.GPS_channels.index(channel_name)
            return c_char2Str(c_char_p(aimXRK.get_GPS_channel_units(self.idxf, idxc)))
        except:
            return 0
            
    def GPS_channel_units_by_index(self, idxc):
            return c_char2Str(c_char_p(aimXRK.get_GPS_channel_units(self.idxf, idxc)))

            
    def GPS_channel_times_and_samples(self, channel_name):
        idxc = self.GPS_channels.index(channel_name)
        sample_count = self.GPS_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_GPS_channel_samples(self.idxf, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def GPS_channel_times_and_samples_by_index(self, idxc):
        sample_count = self.GPS_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_GPS_channel_samples(self.idxf, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def GPS_lap_channel_sample_count(self, channel_name, lap_number):
        idxl = lap_number - 1 
        try:
            idxc = self.GPS_channels.index(channel_name)
            return aimXRK.get_lap_GPS_channel_samples_count(self.idxf, idxl, idxc)
        except:
            return 0
            
    def GPS_lap_channel_sample_count_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        return aimXRK.get_lap_GPS_channel_samples_count(self.idxf, idxl, idxc)
        
    def GPS_lap_channel_times_and_samples(self, channel_name, lap_number):
        idxc = self.GPS_channels.index(channel_name)
        idxl = lap_number - 1
        sample_count = self.GPS_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_lap_GPS_channel_samples(self.idxf, idxl, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def GPS_lap_channel_times_and_samples_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        sample_count = self.GPS_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_lap_GPS_channel_samples(self.idxf, idxl, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    ############################################################################
    ## RAW GPS DATA CHANNEL MEHTODS
    ############################################################################  
        
    def GPS_raw_raw_channel_count(self):
        return aimXRK.get_GPS_raw_raw_channels_count(self.idxf)
        
    def GPS_raw_channel_count(self):
        return aimXRK.get_GPS_raw_channels_count(self.idxf)
        
    def GPS_raw_channel_list(self):
        channel_names = []
        
        for i in range(self.GPS_raw_channel_count()):
            channel_i = c_char2Str(c_char_p(aimXRK.get_GPS_raw_channel_name(self.idxf, i)))
            channel_names.append(channel_i) 
        
        return channel_names
     
    def GPS_raw_channel_sample_count(self, channel_name):
        try:
            idxc = self.GPS_raw_channels.index(channel_name)
            return aimXRK.get_GPS_raw_channel_samples_count(self.idxf, idxc)
        except:
            return 0

    def GPS_raw_channel_sample_count_by_index(self, idxc):
        return aimXRK.get_GPS_raw_channel_samples_count(self.idxf, idxc)
    
    def GPS_raw_channel_units(self, channel_name):
        try:
            idxc = self.GPS_raw_channels.index(channel_name)
            return c_char2Str(c_char_p(aimXRK.get_GPS_raw_channel_units(self.idxf, idxc)))
        except:
            return 0
            
    def GPS_raw_channel_units_by_index(self, idxc):
            return c_char2Str(c_char_p(aimXRK.get_GPS_raw_channel_units(self.idxf, idxc)))

            
    def GPS_raw_channel_times_and_samples(self, channel_name):
        idxc = self.GPS_raw_channels.index(channel_name)
        sample_count = self.GPS_raw_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_GPS_raw_channel_samples(self.idxf, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def GPS_raw_channel_times_and_samples_by_index(self, idxc):
        sample_count = self.GPS_raw_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_GPS_raw_channel_samples(self.idxf, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def GPS_raw_lap_channel_sample_count(self, channel_name, lap_number):
        idxl = lap_number - 1 
        try:
            idxc = self.GPS_raw_channels.index(channel_name)
            return aimXRK.get_lap_GPS_raw_channel_samples_count(self.idxf, idxl, idxc)
        except:
            return 0
            
    def GPS_raw_lap_channel_sample_count_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        return aimXRK.get_lap_GPS_raw_channel_samples_count(self.idxf, idxl, idxc)
        
    def GPS_raw_lap_channel_times_and_samples(self, channel_name, lap_number):
        idxc = self.GPS_raw_channels.index(channel_name)
        idxl = lap_number - 1
        sample_count = self.GPS_raw_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_lap_GPS_raw_channel_samples(self.idxf, idxl, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]
        
    def GPS_raw_lap_channel_times_and_samples_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        sample_count = self.GPS_raw_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (c_double * sample_count)()
        sampleptr = (c_double * sample_count)()
        
        success = aimXRK.get_lap_GPS_raw_channel_samples(self.idxf, idxl, idxc, byref(timeptr), 
                                             byref(sampleptr), sample_count)
        
        for i in range(sample_count):
            times.append(timeptr[i])
            samples.append(sampleptr[i])
        
        return [times, samples]