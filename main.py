from server.ical import EventParser
from server.config import Config


def main():
    """
    Commandline Interface for displayin result sets
    Output in json format can be further processed by datapipelines
    """
    #global_parser.add_argument('--verbose', '-v', action='store_true', help='be verbose')
    #args = global_parser.parse_args()
    ep = EventParser()
    
    print(ep.get_events())

if __name__ == "__main__":
    main()
