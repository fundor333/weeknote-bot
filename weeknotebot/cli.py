import os

import click


def doesFileExists(filePathAndName):
    return os.path.exists(filePathAndName)


@click.command()
@click.option(
    "--configuration",
    "-config",
    default="~/.config/weeknote_bot/config.json",
    type=str,
    required=False,
    help="Path to the configuration file.",
)
def cli(
    configuration: str,
) -> None:
    if doesFileExists(configuration):
        print("Yaa it exists!")
    else:
        print("Nope! Not around")


if __name__ == "__main__":
    cli()
