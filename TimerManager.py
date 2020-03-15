from Timer import Timer

class TimerManager:
 
    def __init__(self):
        self.timers = []
        self.longestNameLen = 0


    def addTimer(self, timerName, timeElapsed, initialTime, area):
        '''adds a timer object to the list'''
        for timer in self.timers: # checks if timer with given name exists
            if timer.name == timerName:
                print('\nError: timer with name', timerName, 'already exists')
                return
        self.timers.append(Timer(timerName, timeElapsed, initialTime, area))
        if len(timerName) > self.longestNameLen:
            self.longestNameLen = len(timerName)


    def deleteTimer(self, timerName):
        '''removes the timer object with the given name from the list'''
        foundMatchingTimer = False
        for timer in self.timers: # looks for timer with matching name
            if timer.name == timerName:
                self.timers.remove(timer)
                foundMatchingTimer = True
        if not foundMatchingTimer:
            print('\nError: timer', timerName, 'does not exist')


    def getTimers(self):
        '''returns a list of the timers'''
        timers = []
        for timer in self.timers:
            timers.append(timer)
        return timers
    

    def getTimerNames(self):
        '''returns a list of the timer names'''
        timerNames = []
        for timer in self.timers:
            timerNames.append(timer.name)
        return timerNames

    
    def getTimer(self, timerName):
        '''returns a timer object with the given name'''
        for timer in self.timers:
            if timer.name == timerName:
                return timer
        return None


    def saveData(self):
        '''writes the current timer data
        to a save file'''
        data = open('SaveData.txt', 'w')
        for timer in self.timers:
            string = timer.name + ',' + str(timer.timeElapsed) + ',' + str(timer.initialTime) + ',' + str(timer.area) + '\n'
            data.write(string)
        data.close()


    def loadData(self):
        '''populates timer list with timer objects
        according to the attributes in the save file'''
        try:
            data = open('SaveData.txt', 'r')
        except:
            print('\nNo save data found')
        else:
            failed = False
            for line in data:
                if line.strip() == '':
                    continue
                args = line.split(',')
                try:
                    args[1] = float(args[1].strip())
                    args[2] = float(args[2].strip())
                    args[3] = args[3].strip()
                    if args[3] == 'None':
                        args[3] = None
                except:
                    failed = True
                else:
                    self.addTimer(args[0], args[1], args[2], args[3])
            if failed:
                print('\nError: file does not follow the expected format')
            data.close()