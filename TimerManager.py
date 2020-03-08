from Timer import Timer

class TimerManager:
 
    def __init__(self):
        self.timers = []
        self.longestNameLen = 0


    def addTimer(self, timerName, timeElapsed, initialTime):
        for timer in self.timers: # checks if timer with given name exists
            if timer.name == timerName:
                print('\nError: timer with name', timerName, 'already exists')
                return
        self.timers.append(Timer(timerName, timeElapsed, initialTime))
        if len(timerName) > self.longestNameLen:
            self.longestNameLen = len(timerName)


    def deleteTimer(self, timerName):
        foundMatchingTimer = False
        for timer in self.timers: # looks for timer with matching name
            if timer.name == timerName:
                self.timers.remove(timer)
                foundMatchingTimer = True
        if not foundMatchingTimer:
            print('\nError: timer', timerName, 'does not exist')


    def getTimers(self):
        timers = []
        for timer in self.timers:
            timers.append(timer)
        return timers
    

    def getTimerNames(self):
        timerNames = []
        for timer in self.timers:
            timerNames.append(timer.name)
        return timerNames


    def saveData(self):
        data = open('SaveData.txt', 'w')
        for timer in self.timers:
            string = timer.name + ',' + str(timer.timeElapsed) + ',' + str(timer.initialTime) + '\n'
            data.write(string)
        data.close()


    def loadData(self):
        try:
            data = open('SaveData.txt', 'r')
        except:
            print('\nNo save data found')
        else:
            for line in data:
                args = line.split(',')
                try:
                    args[1] = float(args[1])
                    args[2] = float(args[2])
                    self.addTimer(args[0], args[1], args[2])
                except:
                    print('\nError: file does not follow the expected format')
            data.close()