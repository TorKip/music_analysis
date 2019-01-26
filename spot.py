import aggregate
import sys


help_text = {
    "general": "here will be help soon"
}


def welcome_info():
    version = 0.0
    welcome = "Velkommen til <ubestemt navn>"
    help = help_text["general"]
    print("{} \n Versjon nummer: {} \n {}".format(welcome, version, help))


if __name__ == "__main__":
    parameters = sys.argv[1:] if len(sys.argv) > 1 else None
    print("Running \"spot if i\" why with parameters:{}".format(parameters))
    if not parameters:
        print(welcome_info())
    while parameters:
        parameter = parameters.pop(0)
        if parameter == "--aggregate" or parameter == "-A":
            parameter = parameters.pop(0) if len(parameters) > 0 else None
            if parameter == "--spotify" or parameter == "-s":
                aggregate.create_history('spotify')
            elif parameter == "--lastfm" or parameter == "-lfm":
                aggregate.create_history('lastfm')
            elif not parameter:
                aggregate.create_history()
            elif parameter == "--help" or parameter == "-h":
                print("here comes help soon")
            else:
                print("for help type --help or -h")
        elif parameter == '--mute' or parameter == "-m":
            pass
        elif parameter == "--help" or parameter == "-h":
            pass
        elif parameter == "--process" or parameter == "-P":
            aggregate.process_statistics()
    # process_statistics('StreamingHistory.json')
