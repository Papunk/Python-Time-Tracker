import time
from enum import Enum
# import matplotlib
# import tkinter as tk

class Timer:

    def __init__(self, name, timeElapsed, initialTime):
        self.name = name
        self.timeElapsed = timeElapsed
        self.initialTime = initialTime
        if initialTime == 0:
            self.isActive = False
        else:
            self.isActive = True


    def startTimer(self):
        '''gets the current system time in seconds'''
        self.timeElapsed = 0
        self.initialTime = time.time()
        self.isActive = True


    def endTimer(self):
        '''returns the time elapsed since the timer
        was started in seconds as an integer'''
        self.timeElapsedFormatted = self.getTimeElapsed()
        self.initialTime = 0 
        self.isActive = False


    def getTimeElapsed(self):
        if self.isActive:
            self.timeElapsed = time.time() - self.initialTime
            return self.timeToString(round(self.timeElapsed))
        else:
            return self.timeToString(round(self.timeElapsed))

    
    def logData(self, time):
        try:
            time = int(time)
            self.timeElapsed += time
        except:
            time = self.stringToTime(time)
            if time == None:
                print('\nError: Invalid time format')
            else:
                self.timeElapsed += time


    def stringToTime(self, string):
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


class Parser:

    class KeyWords(Enum):
        SYNTAX = 'syntax'
        MAKE = 'make'
        DEL = 'delete'
        START = 'start'
        STOP = 'stop'
        RESET = 'reset'
        SHOW = 'show'
        QUIT = 'quit'
        LOG = 'log'
        SET = 'set'


    def __init__(self, tm):
        self.tm = tm


    def parse(self, text):
        '''sends the arguments to the various functions'''
        text = self.separate(text.strip())
        command = text['command']
        arguments = text['arguments']

        if command != None:
            # loops for the keyword used
            if command == self.KeyWords.SYNTAX.value:
                self.syntaxGuide()
            elif command == self.KeyWords.MAKE.value:
                self.make(arguments)
            elif command == self.KeyWords.DEL.value:
                self.delete(arguments)
            elif command == self.KeyWords.START.value:
                self.start(arguments)
            elif command == self.KeyWords.STOP.value:
                self.stop(arguments)
            elif command == self.KeyWords.RESET.value:
                self.reset(arguments)
            elif command == self.KeyWords.SHOW.value:
                self.show()
            elif command == self.KeyWords.QUIT.value:
                self.end()
            elif command == self.KeyWords.LOG.value:
                self.logTime(arguments)
            elif command == self.KeyWords.SET.value:
                self.setTime(arguments)
        else:
            print('\nInvalid command')


    def separate(self, text):
        command = None
        arguments = None
        # iterates over the acceptable keywords
        for keyWord in self.KeyWords: 
            # checks if the command is valid
            if text.lower().startswith(keyWord.value):
                spacePos = text.find(' ')
                if spacePos != -1:
                    command = text[:spacePos].lower()
                    arguments = text[spacePos+1:].lstrip()
                    # if multiple arguments are given, divide the arguments
                    if ',' in arguments:
                        arguments = arguments.split(',')
                        # strips elements of trailing and leading whitespace
                        for i in range(len(arguments)):
                            arguments[i] = arguments[i].strip() 
                    else:
                        arguments = [arguments]
                else:
                    command = text.lower()
        return {'command':command, 'arguments':arguments}


    def syntaxGuide(self):
        print()
        try:
            syntax = open('SyntaxGuide.txt', 'r')
        except:
            print('\nError: File not found')
        else:
            for line in syntax:
                print(line) 
            syntax.close()   


    def make(self, args):
        if args != None:
            for arg in args:
                self.tm.addTimer(arg, 0, 0)
            self.show()
        else:
            print('\nNo arguments provided')


    def delete(self, args):
        if args != None:
            for arg in args:
                self.tm.deleteTimer(arg)
            self.show()
        else:
            validation = input('\nAre you sure you want to delete all timers? This action cannot be undone. (y/n) ')
            if validation.lower() == 'y':
                for timer in self.tm.getTimers():
                    self.tm.deleteTimer(timer.name)
                print('\nAll timers deleted')
            else:
                print('\nAborted')


    def start(self, args):
        if len(self.tm.timers) > 0:
            if args == None:
                for timer in self.tm.timers:
                    if not timer.isActive:
                        timer.startTimer()
            else:
                for timer in self.tm.timers:
                    if timer.name in args:
                        args.remove(timer.name)
                        if not timer.isActive:
                            timer.startTimer()
                if len(args) > 0:
                    print('\nCould not find:')
                    for arg in args:
                        print(arg)
            self.show()
        else:
            print('\nNo timers found')


    def stop(self, args):
        if len(self.tm.timers) > 0:
            if args == None:
                for timer in self.tm.timers:
                    if timer.isActive:
                        timer.endTimer()
            else:
                for timer in self.tm.timers:
                    if timer.name in args:
                        args.remove(timer.name)
                        if timer.isActive:
                            timer.endTimer()
                if len(args) > 0:
                    print('\nCould not find:')
                    for arg in args:
                        print(arg)
            self.show()
        else:
            print('\nNo timers found')
            

    def reset(self, args):
        if len(self.tm.timers) != 0:
            if args != None:
                for timer in self.tm.timers:
                    if timer.name in args:
                        timer.isActive = False
                        timer.timeElapsed = 0
                        timer.initialTime = 0
            else:
                validation = input('\nAre you sure you want to reset all timers? This action cannot be undone. (y/n) ')
                if validation.lower() == 'y':
                    for timer in self.tm.timers:
                        timer.isActive = False
                        timer.timeElapsed = 0
                        timer.initialTime = 0
                else:
                    print('\nAborted')
            self.show()
        else:
            print('\nNo timers found')


    def timerInfo(self, timer):
        if timer.isActive:
            status = 'active  '
        else:
            status = 'inactive'
        spaceLen = self.tm.longestNameLen - len(str(timer.name))
        space = ''
        for _ in range(spaceLen):
            space += ' '

        print(timer.name + space, '|', status, '|', timer.getTimeElapsed())


    def show(self):
        print()
        if len(self.tm.timers) > 0:
            for timer in self.tm.timers:
                self.timerInfo(timer)
        else:
            print('No timers to show')

    
    def end(self):
        self.tm.saveData()
        exit()


    def parsePair(self, cmd, word):
        cmd = cmd.split()
        if len(cmd) < 2:
            print('\nNeed two arguments. Please follow format: "' + word + ' HH:MM:SS timerName"')
            return None
        elif len(cmd) > 2:
            newName = ''
            for word in cmd[1:]:
                newName += word + ' '
            cmd = [cmd[0], newName.rstrip()]
        return cmd


    def logTime(self, args):
        cmds = {}
        for arg in args:
            cmd = self.parsePair(arg, 'log')
            if cmd != None:
                cmds[cmd[1]] = cmd[0]

        found = 0
        for timer in self.tm.timers:
            if timer.name in cmds.keys():
                timer.logData(cmds[timer.name])
                found += 1
        if found < len(cmds):
            print('\n' + str(len(cmds) - found), 'timer(s) not found')
        self.show()


    def setTime(self, args):
        pass










def opening():
    print()
    print('Python Time Tracker')
    print('–––––––––––––––v1.3')


def main():
    opening()

    name = 'User'
    prompt = '\n' + name + ': '
    programIsRunning = True

    manager = TimerManager()
    parser = Parser(manager)

    manager.loadData()
    while programIsRunning:
        command = input(prompt)
        parser.parse(command)
        manager.saveData()


main()



