import time
from Errors import *

class Timer:

    def __init__(self, name, timeElapsed, initialTime, area):
        '''
        Desc:
            This class defines the properties and functions needed to run a time tracker
        
        Arguments:
            name (string) - the name of the timer
            timeElapsed (int) - this is the amount of time the timer has tracked
            initialTime (int) - if the timer is active, this is the time when it was first set to run
            area (string) - the name of the area that the timer belongs to
        '''
        self.name = name
        self.timeElapsed = timeElapsed
        self.initialTime = initialTime
        if initialTime == 0:
            self.isActive = False
        else:
            self.isActive = True
        self.area = area
        

    def startTimer(self):
        '''
        Desc:
            Saves the system nanotime and starts timer
        '''
        self.initialTime = time.time()
        self.isActive = True


    def endTimer(self):
        '''
        Desc:
            Saves the time elapsed since the timer was started as an integer in seconds stops the timer
        '''
        self.timeElapsed += (time.time() - self.initialTime)
        self.initialTime = 0 
        self.isActive = False


    def getTimeElapsed(self):
        '''
        Desc:
            Returns time elapsed without stopping the timer
        '''
        if self.isActive:
            self.timeElapsed += (time.time() - self.initialTime)
            self.initialTime = time.time()
        if self.isActive:
            return self.timeToString(round(self.timeElapsed))
        else:
            return self.timeToString(round(self.timeElapsed))

    
    def logData(self, time):
        '''
        Desc:
            Adds input value to the time elapsed

        Arguments:
            time (int, string) - the time in seconds or in HH:MM:SS format

        Raises:
            InvalidTimeFormatException
        '''
        try: # time in seconds
            time = int(time)
            self.timeElapsed += time
        except: # time as a string
            time = self.stringToTime(time)
            if time == None:
                raise InvalidTimeFormatException
            else:
                self.timeElapsed += time


    def setData(self, time):
        '''
        Desc:
            changes the time elapsed to the input value
        
        Arguments:
            time (int, string) - the time in seconds or in HH:MM:SS format

        Raises:
            InvalidTimeFormatException
        '''
        try:
            time = int(time)
            self.timeElapsed = time
        except:
            time = self.stringToTime(time)
            if time == None:
                raise InvalidTimeFormatException
            else:
                self.timeElapsed = time


    def stringToTime(self, time):
        '''
        Desc:
            Turns a string in HH:MM:SS format into seconds

        Arguments:
            time (string) - the time in HH:MM:SS format
        
        Returns:
            int

        Raises:
            InvalidTimeFormatException
        '''
        sep1 = time.find(':')
        sep2 = time.find(':', sep1 + 1)
        if sep1 == -1 or sep2 == -2:
            raise InvalidTimeFormatException
        else:
            try:
                h = int(time[:sep1])
                m = int(time[sep1+1:sep2])
                s = int(time[sep2+1:])
            except:
                raise InvalidTimeFormatException
            if h < 0 or m >= 60 or m < 0 or  s >= 60 or s < 0:
                raise InvalidTimeFormatException
            else:
                return (h * 3600) + (m * 60) + s


    def timeToString(self, time):
        '''
        Desc:
            Turns time in seconds into a string in HH:MM:SS format
            
        Arguments:
            time (int) - time in seconds as an integer

        Return:
            string in HH:MM:SS format
        '''
        try:
            time = int(time)
        except ValueError:
            raise InvalidTimeFormatException

        if time < 0:
           raise InvalidTimeFormatException

        if self.isActive:
            placeHol = '00'
        else:
            placeHol = '--'

        if time > 3600:
            h = str(s // 3600)
            m = str(int(s % 3600) // 60)
            s = str(int((s % 3600) % 60))
        elif time > 60:
            h = placeHol
            m = str(s // 60)
            s = str(int(s % 60))
        elif time > 0:
            h = placeHol
            m = placeHol
            s = str(s)
        else:
            h = placeHol
            m = placeHol
            s = placeHol

        if len(h) < 2:
            h = '0' + h
        if len(m) < 2:
            m = '0' + m
        if len(s) < 2:
            s = '0' + s

        return h + ':' + m + ':' + s