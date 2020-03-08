from Parser import Parser
from TimerManager import TimerManager


def opening():
    print()
    print('Python Time Tracker')
    print('–––––––––––––––v1.8')


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



