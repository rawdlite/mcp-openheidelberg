import argparse
from server.ical import EventParser
from server.workpackages import WorkPackageParser




def main():
    """
    Commandline Interface for displayin result sets
    Output in json format can be further processed by datapipelines
    """
    parser = argparse.ArgumentParser()
    #Todo: improve argparser to showw valid commands
    #parser.add_argument('--verbose', '-v', action='store_true', help='be verbose')
    parser.add_argument('command', type=str, help='execute command')
    args = parser.parse_args()
    if args.command == 'events':
        ep = EventParser()
        print(ep.get_events())
    elif args.command == 'tasks':
        wp = WorkPackageParser()
        print(wp.get_workpackages())
    elif args.command == 'members':
        wp = WorkPackageParser()
        print(wp.get_members())
    else:
        print("command (events,tasks,members) requiered")

if __name__ == "__main__":
    main()
