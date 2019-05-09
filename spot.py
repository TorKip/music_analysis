import click
import track_record.tests.test_main as test_main
from track_record.postprocess import aggregate as aggregate_history,\
        visualize as visualize_history
from track_record.preprocess import preprocess as preprocess_history


# @click.command()
# @click.option("--variable", default="default_world",
#                 help="variable, is string")
# @click.option("--repeat", default=1)
# def cli(variable):
#     """Example script"""
#     click.echo("Hello all! This good: cli, string is {}".format(variable))

@click.group()
@click.version_option()
def cli():
    """Entry point for the general program"""
    pass


@click.command(help="Run tests")
@click.option('-A', '--all',
              help="Run all tests", is_flag=True, default=False)
# @click.argument("tests", nargs=1)
def test(all):
    """Runs tests based on given options"""
    if all:
        test_main.run_all()
#     click.echo(all)


@click.command('postprocess', help="Process music history")
@click.option("-s", "--spotify", "source",
              help="Use spotify history as source", flag_value="spotify")
@click.option("-lfm", "--lastfm", "source",
              help="Use lastfm history as source", flag_value="lastfm")
def postprocess(source):
    """Command to process data with different opptions"""
    if source:
        aggregate_history.create_history(source)
    else:
        aggregate_history.create_history()


@click.group('preprocess', help="Preprocess and clean imported data.")
@click.option("-fd", "--filldatabase", is_flag=True, default=False,
              help="Fills database with data at default path")
def preprocess(filldatabase):
    """Group of commands to preprocess data with different options"""
    if filldatabase:
        preprocess_history.fill_database()


@click.command("clean_data", help="Clean imported data from chosen source")
@click.option("--source_format", type=click.Choice(["spotify", "lastfm"]),
              help="Default source format = LastFM", default="lastfm")
@click.argument("source",
                default="track_record/music_history/LastFmTest.json")
def clean_data(source, source_format):
    """Clean imported data from chosen source. Default: lastfm"""
    click.echo("Cleaning data on path: {} \nUsing format: {}"
               .format(source, source_format))
    if source:
        preprocess_history.save_clean_data(source, source_format)


# @click.option("-fd", "--filldatabase", is_flag=True, default=False,
#               help="Fills database with data at default path")
@click.command("fill_database")
@click.argument("source",
                default="track_record/music_history/cleanlfm.json")
@click.argument("path", 
                default="history.db")
def fill_database(source, path):
    """Fills database at path with cleaned data at source. 
    
    Default path: history.db
    
    Default source: track_record/music_history/cleanlfm.json
    """
    click.echo("Filling database {} with data from {}"
               .format(path, source))
    preprocess_history.fill_database(source, path)


@click.command("visualize", help="Creates visualisations of processed data.")
@click.option("-SO", "--static_out", is_flag=True, default=False)
def visualize(static_out):
    """Command to give visualisations based on processed data"""
    if static_out:
        visualize_history.static_out()


cli.add_command(test)
cli.add_command(postprocess)
cli.add_command(preprocess)
cli.add_command(visualize)

preprocess.add_command(clean_data)
preprocess.add_command(fill_database)
