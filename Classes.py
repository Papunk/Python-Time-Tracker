import time
import matplotlib
import tkinter as tk
from enum import Enum

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
                break
        self.timers.append(Timer(timerName, 0, 0))
        if len(timerName) > self.longestNameLen:
            self.longestNameLen = len(timerName)


    def deleteTimer(self, timerName):
        foundMatchingTimer = False
        for timer in self.timers: # looks for timer with matching name
            if timer.name == timerName:
                self.timers.remove(timer)
                del timer
                foundMatchingTimer = True
        if not foundMatchingTimer:
            print('\nError: timer', timerName, 'does not exist')


    def getTimers(self):
        return self.timers

    def saveData(self):
        data = open('SaveData.txt', 'w')
        for timer in self.timers:
            string = timer.name + ',' + str(timer.timeElapsed) + ',' + str(timer.initialTime) + '\n'
            print(string)
            data.write(string)
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


    def __init__(self, tm):
        self.tm = tm


    def parse(self, text):
        '''sends the arguments to the various functions'''
        text = self.separate(text.strip())
        command = text['command']
        arguments = text['arguments']

        if text != None:
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
        else:
            print('invalid command:', command)


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
                    command = text
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
        if isinstance(args, str):
            self.tm.addTimer(args, 0, 0)
        elif isinstance(args, list):
            for arg in args:
                self.tm.addTimer(arg, 0, 0)
        else:
            print('Unknown error occurred in Parser.make()')
        self.show()


    def delete(self, args):
        if isinstance(args, str):
            self.tm.deleteTimer(args)
        elif isinstance(args, list):
            for arg in args:
                self.tm.deleteTimer(arg)
        else:
            print('Unknown error occurred in Parser.delete()')
        self.show()


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
        for timer in self.tm.timers:
            if timer.name in args:
                timer.isActive = False
                timer.timeElapsed = 0


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






def main():
    name = 'Papunk'
    command = ''
    prompt = '\n' + name + ': '
    programIsRunning = True

    manager = TimerManager()
    parser = Parser(manager)

    
    while programIsRunning:
        command = input(prompt)

        parser.parse(command)


main()



