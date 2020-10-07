from Timer import Timer

class TimerManager:
 
    def __init__(self):
        '''
        Desc:
            Handles timers and their respective areas
        '''
        self.timers = []
        self.longestNameLen = 0


    def addTimer(self, timerName, timeElapsed, initialTime, area):
        '''
        Desc:
            Adds a timer object to the list of timers

        Arguments:
            timerName (string) - the name of the timer
            timeElapsed (int) - this is the amount of time the timer has tracked
            initialTime (int) - if the timer is active, this is the time when it was first set to run
            area (string) - the name of the area that the timer belongs to 
        '''
        for timer in self.timers: # checks if timer with given name exists
            if timer.name == timerName:
                print('Timer with name', timerName, 'already exists')
        self.timers.append(Timer(timerName, timeElapsed, initialTime, area))
        if len(timerName) > self.longestNameLen:
            self.longestNameLen = len(timerName)


    def deleteTimer(self, timerName):
        '''
        Desc:
            Removes the timer object with the given name from the list
        
        Arguments:
            timerName (string) - the name of the timer
        '''
        foundMatchingTimer = False
        for timer in self.timers: # looks for timer with matching name
            if timer.name == timerName:
                self.timers.remove(timer)
                foundMatchingTimer = True
        if not foundMatchingTimer:
            print('\nError: timer', timerName, 'does not exist')


    def getTimers(self):
        '''
        Desc:
            Returns a list of all existing timers

        Returns:
            [Timer]
        '''
        timers = []
        for timer in self.timers:
            timers.append(timer)
        return timers
    

    def getTimerNames(self):
        '''
        Desc:
            Returns a list of the timer names
        
        Returns:
            [String]
        '''
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
        '''
        Desc:
            Writes the current timer data to a save file
        '''
        data = open('SaveData.txt', 'w')
        for timer in self.timers:
            string = timer.name + ',' + str(timer.timeElapsed) + ',' + str(timer.initialTime) + ',' + str(timer.area) + '\n'
            data.write(string)
        data.close()


    def loadData(self):
        '''
        Desc:
            Populates the timer list with timer objects according to the attributes in the save file
        '''
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