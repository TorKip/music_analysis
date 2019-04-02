import sys
from track_record.preprocess import preprocess
from track_record.postprocess import aggregate, visualize
from track_record.utils import db_tools, spot_utils
from track_record.tests import test_main


help_text = {
    "general": "here will be help soon",
    "commands":{
        "aggregate": "to aggregate add attributes:  --aggregate|-A  and -s|-lfm ",
        "preprocess": "to preprocess add attributes: --preprocess|-pp and -lfm "
        }
}


def welcome_info():
    version = 0.1
    welcome = "Velkommen til <ubestemt navn>"
    help = help_text["general"]
    print("{} \n Versjon nummer: {} \n {}".format(welcome, version, help))


if __name__ == "__main__":
    parameters = sys.argv[1:] if len(sys.argv) > 1 else None
    print("Running \"spot if I\" why with parameters:{}".format(parameters))
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
                print(help_text["commands"]["aggregate"])
            else:
                print("for help type --help or -h")

        elif parameter == '--mute' or parameter == "-m":
            pass
        elif parameter == "--help" or parameter == "-h":
                print(help_text["general"])

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
                print(help_text["commands"]["preprocess"])
            else:
                print("for help type --help or -h")
        
        elif parameter == "--filldatabase" or preprocess == "-fd":
            preprocess.fill_database()

        elif parameter == "--process" or parameter == "-P":
            aggregate.process_statistics()

        elif parameter == "--output" or parameter == "-O":
            visualize.static_out()

        elif parameter == "--test" or parameter == "-T":
            test_main.run()
            
        elif parameter == "-stest":
            print(spot_utils.get_spotify_id(artist="ABBA"))
    # process_statistics('StreamingHistory.json')
