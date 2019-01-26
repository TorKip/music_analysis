import aggregate
import sys
import preprocess


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
    if not parameters:
        print(welcome_info())
    print(parameters)
    while parameters:
        parameter = parameters.pop(0)
        if parameter == "--aggregate" or parameter == "-A":
            parameter = parameters.pop() if len(parameters) > 0 else None
            if parameter == "--spotify" or parameter == "-s":
                pass
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
                print("here comes help soon")

        elif parameter == "--preprocess" or parameter == "-pp":
            
            parameter = parameters.pop(0) if len(parameters) > 0 else None
            if parameter == "--spotify" or parameter == "-s":
                pass
                preprocess.save_clean_data('spotify')
            elif parameter == "--lastfm" or parameter == "-lfm":
                print("Creating cleaned copy of LFM data...")
                preprocess.save_clean_data('lastfm')
                print("Done!")
            elif parameter == "--help" or parameter == "-h" or not parameter:
                print("here comes help soon")
            else:
                print("for help type --help or -h")

        elif parameter == "--process" or parameter == "-P":
            aggregate.process_statistics()
    # process_statistics('StreamingHistory.json')
