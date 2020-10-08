from TimerManager import TimerManager
from enum import Enum # no need for these

'''
THE IMPLEMENTATION OF SOME FUNCTIONS
HERE IS A BIT CLUMSY, NEED TO WORK ON THAT
'''

class Parser:

    class KeyWords(Enum):
        # turn this into a dictionary
        '''allowed keywords for commands'''

        SYNTAX = 'syntax'
        # Commands
        MAKE = 'make'
        SHORTHAND_MAKE = '-m'
        DEL = 'delete'
        SHORTHAND_DEL = '-d'
        START = 'start'
        SHORTHAND_START = '-s'
        STOP = 'stop'
        SHORTHAND_STOP = '-x'
        RESET = 'reset'
        SHORTHAND_RESET = '-r'
        SHOW = 'show'
        QUIT = 'quit'
        SHORTHAND_QUIT = '-q'
        LOG = 'log'
        SET = 'set'
        # Area Management
        AREA = 'area'
        SHORTHAND_AREA = '-a'
        ROOT = 'root'


    def __init__(self, tm):
        self.tm = tm


    def parse(self, text):
        '''sends the arguments to the various functions'''
        text = self.separate(text.strip())
        command = text['command']
        arguments = text['arguments']

        # this is impressively awful, use a loop
        if command != None:
            # loops for the keyword used
            if command == self.KeyWords.SYNTAX.value:
                self.syntaxGuide()
            elif command == self.KeyWords.MAKE.value or command == self.KeyWords.SHORTHAND_MAKE.value:
                self.make(arguments)
            elif command == self.KeyWords.DEL.value or command == self.KeyWords.SHORTHAND_DEL.value:
                self.delete(arguments)
            elif command == self.KeyWords.START.value or command == self.KeyWords.SHORTHAND_START.value:
                self.start(arguments)
            elif command == self.KeyWords.STOP.value  or command == self.KeyWords.SHORTHAND_STOP.value:
                self.stop(arguments)
            elif command == self.KeyWords.RESET.value or command == self.KeyWords.SHORTHAND_RESET.value:
                self.reset(arguments)
            elif command == self.KeyWords.SHOW.value:
                self.show()
            elif command == self.KeyWords.QUIT.value or command == self.KeyWords.SHORTHAND_QUIT.value:
                self.end()
            elif command == self.KeyWords.LOG.value:
                self.logTime(arguments)
            elif command == self.KeyWords.SET.value:
                self.setTime(arguments)
            elif command == self.KeyWords.AREA.value or command == self.KeyWords.SHORTHAND_AREA.value:
                self.addToArea(arguments)
            elif command == self.KeyWords.ROOT.value:
                self.root(arguments)
            else:
                print('\nInvalid command:', command)
        else:
            print('\nInvalid command')


    def separate(self, text):
        # needs to be reworked
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


# gonna need a far more sophisticated parser than this

    def syntaxGuide(self):
        print()
        try:
            syntax = open('SyntaxGuide.txt', 'r')
        except:
            print('\nError: File not found')
        else:
            for line in syntax:
                print(line.rstrip()) 
            syntax.close()   


    def make(self, args):
        if args != None:
            for arg in args:
                self.tm.addTimer(arg, 0, 0, None)
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
                self.show()
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
                else:
                    self.show()
        else:
            print('\nNo timers found')


    def stop(self, args):
        if len(self.tm.timers) > 0:
            if args == None:
                for timer in self.tm.timers:
                    if timer.isActive:
                        timer.endTimer()
                self.show()
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
                else:
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
            seq = '\033[0m' # bold, brighter color
        else:
            status = 'inactive'
            seq = '\033[37m' # dimmer color
        spaceLen = self.tm.longestNameLen - len(str(timer.name))
        space = ''
        for _ in range(spaceLen):
            space += ' '
        print(seq + timer.name + space, '|', status, '|', timer.getTimeElapsed() + '\033[0m')


    def show(self):
        timers = self.tm.getTimers()
        if len(timers) > 0:
            areas = {}
            for timer in timers:
                if timer.area == None:
                    if 'Timers' not in areas.keys():
                        areas['Timers'] = [timer]
                    else:
                        areas['Timers'].append(timer)
                else:
                    if timer.area not in areas.keys():
                        areas[timer.area] = [timer]
                    else:
                        areas[timer.area].append(timer)
            for area, timers in areas.items():
                print('\n\033[1m' + area + '\033[0m')
                line = ''
                for _ in range(len(area)):
                    line += '–'
                print(line.rstrip())
                for timer in timers:
                    self.timerInfo(timer)
        else:
            print('\nNo timers to show')
        
  
    def end(self):
        self.tm.saveData()
        print()
        exit()
        

    def parsePair(self, cmd):
        cmd = cmd.split()
        if len(cmd) < 2:
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
            cmd = self.parsePair(arg)
            if cmd != None:
                cmds[cmd[1]] = cmd[0]
            else:
                print('\nNeed two arguments.')
        found = 0
        for timer in self.tm.timers:
            if timer.name in cmds.keys():
                timer.logData(cmds[timer.name])
                found += 1
        if found < len(cmds):
            print('\n' + str(len(cmds) - found), 'timer(s) not found')
        else:
            self.show()


    def setTime(self, args):
        cmds = {}
        for arg in args:
            cmd = self.parsePair(arg)
            if cmd != None:
                cmds[cmd[1]] = cmd[0]
            else:
                print('\nNeed two arguments.')
        found = 0
        for timer in self.tm.timers:
            if timer.name in cmds.keys():
                timer.setData(cmds[timer.name])
                found += 1
        if found < len(cmds):
            print('\n' + str(len(cmds) - found), 'timer(s) not found')
        else:
            self.show()

    
    def addToArea(self, args):
        if args == None:
            print('\nNo arguments given')
        elif len(self.tm.timers) > 0:
            for arg in args:
                cmd = self.parsePair(arg)
                if cmd != None:
                    timer = self.tm.getTimer(cmd[1])
                    if timer != None:
                        timer.area = cmd[0]
                    else:
                        print('\nTimer with name', cmd[1], 'not found')
                        return
                elif len(args) == 1:
                    for timer in self.tm.timers:
                        timer.area = args[0]
            self.show()
        else:
            print('\nNo timers found')

    def root(self, args):
        pass

