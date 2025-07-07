import argparse
from server.ical import EventParser
from server.workpackages import WorkPackageParser




def main():
    """
    Commandline Interface for displayin result sets
    Output in json format can be further processed by datapipelines
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true', help='be verbose')
    parser.add_argument('command', type=str, help='execute command')
    args = parser.parse_args()
    if args.command == 'ical':
        ep = EventParser()
        print(ep.get_events())
    elif args.command == 'wp':
        wp = WorkPackageParser()
        print(wp.get_workpackages())
    elif args.command == 'member':
        wp = WorkPackageParser()
        print(wp.get_members())
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
