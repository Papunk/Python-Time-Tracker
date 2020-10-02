import time
import Errors

class Timer:

    def __init__(self, name, timeElapsed, initialTime, area):
        self.name = name
        self.timeElapsed = timeElapsed
        self.initialTime = initialTime
        if initialTime == 0:
            self.isActive = False
        else:
            self.isActive = True
        self.area = area
        

    def startTimer(self):
        '''gets the system nanotime'''
        self.initialTime = time.time()
        self.isActive = True


    def endTimer(self):
        '''gets the time elapsed since the timer was started as an integer in seconds'''
        self.timeElapsed += (time.time() - self.initialTime)
        self.initialTime = 0 
        self.isActive = False


    def getTimeElapsed(self):
        '''returns time elapsed without stopping the timer'''
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
            time - the time in seconds or as a string in HH:MM:SS format

        Raises:
            InvalidTimeFormatError
        '''
        try: # time in seconds
            time = int(time)
            self.timeElapsed += time
        except: # time as a string
            time = self.stringToTime(time)
            if time == None:
                raise Errors.InvalidTimeFormat
            else:
                self.timeElapsed += time


    def setData(self, time):
        '''
        Desc:
            changes the time elapsed to the input value
        
        Arguments:
            time - the time in seconds or as a string in HH:MM:SS format

        Raises:
            InvalidTimeFormatError
        '''
        try:
            time = int(time)
            self.timeElapsed = time
        except:
            time = self.stringToTime(time)
            if time == None:
                raise Errors.InvalidTimeFormat
            else:
                self.timeElapsed = time


    def stringToTime(self, string):
        '''turns a string in
        HH:MM:SS format into seconds'''
        sep1 = string.find(':')
        sep2 = string.find(':', sep1 + 1)
        if sep1 == -1 or sep2 == -2:
            return None
        else:
            try:
                h = int(string[:sep1])
                m = int(string[sep1+1:sep2])
                s = int(string[sep2+1:])
            except:
                return None
            if h < 0 or m >= 60 or m < 0 or  s >= 60 or s < 0:
                return None
            else:
                return (h * 3600) + (m * 60) + s


    def timeToString(self, s):
        '''turns time in seconds
        into a string in HH:MM:SS format'''
        if self.isActive:
            placeHol = '00'
        else:
            placeHol = '--'

        if s > 3600:
            h = str(s // 3600)
            m = str(int(s % 3600) // 60)
            s = str(int((s % 3600) % 60))
        elif s > 60:
            h = placeHol
            m = str(s // 60)
            s = str(int(s % 60))
        elif s > 0:
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