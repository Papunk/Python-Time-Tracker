from TimerManager import TimerManager
from enum import Enum

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
        print()
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
        cmds = {}
        for arg in args:
            cmd = self.parsePair(arg, 'set')
            if cmd != None:
                cmds[cmd[1]] = cmd[0]

        found = 0
        for timer in self.tm.timers:
            if timer.name in cmds.keys():
                timer.setData(cmds[timer.name])
                found += 1
        if found < len(cmds):
            print('\n' + str(len(cmds) - found), 'timer(s) not found')
        self.show()