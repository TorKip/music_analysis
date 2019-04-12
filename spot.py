import click
import track_record.tests.test_main as test_main
from track_record.postprocess import aggregate as aggregate_history, visualize as visualize_history
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
    pass

@click.command(help="run tests")
@click.option('-A','--all', help="What tests to test", is_flag=True, default=False)
# @click.argument("tests", nargs=1)
def test(all):
    if all:
        test_main.run_all()
    click.echo(all)

@click.command('postprocess', help="Process music history")
@click.option("-s", "--spotify", "source", help="Use spotify history as source", flag_value="spotify")
@click.option("-lfm", "--lastfm", "source", help="Use lastfm history as source", flag_value="lastfm")
def postprocess(source):
    if source:
        aggregate_history.create_history(source)
    else:
        aggregate_history.create_history()
    
@click.group('preprocess', help="Preprocess and clean imported data.")
@click.option("-fd", "--filldatabase", is_flag=True, default=False)
def preprocess(filldatabase):
    if filldatabase:
        preprocess_history.fill_database()

# @click.option("-s", "--spotify", "source", help="Clean imported spotify data", flag_value="spotify")
# @click.option("-lfm", "--lastfm", "source", help="Clean imported lastfm data", flag_value="lastfm", default="lastfm")

@click.command("clean_data", help="Clean imported data from chosen source")
@click.option("--source", type=click.Choice(["spotify", "lastfm"]), help="Default source = LastFM")
def clean_data(source):
    """Clean imported data from chosen source. Default: lastfm"""
    if source:
        preprocess_history.save_clean_data(source)


@click.command("visualize", help="Creates visualisations of processed data.")
@click.option("-SO", "--static_out", is_flag=True, default=False)
def visualize(static_out):
    if static_out:
        visualize_history.static_out()
        


cli.add_command(test)
cli.add_command(postprocess)
cli.add_command(preprocess)
cli.add_command(visualize)

preprocess.add_command(clean_data)
