import json
import logging
import os
from pathlib import Path

import click
from rich.logging import RichHandler

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


FORMAT = "%(message)s"
logging.basicConfig(
    level=LOG_LEVEL, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")

DEFAULT_CONFIG = {
    "feeds": [
        {
            "title": "My new post from my blog",
            "url": "https://www.fundor333.com/index.xml",
        },
        {
            "title": "My new post from my newsletter",
            "url": "https://newsletter.digitaltearoom.com/rss/",
        },
    ]
}


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
        log.debug("Yaa I find the config")
    else:
        log.warning("Nope! Generating a new config")

        output_file = Path(configuration)
        output_file.parent.mkdir(exist_ok=True, parents=True)
        with open(output_file, "w") as f:
            json.dump(DEFAULT_CONFIG, f)


if __name__ == "__main__":
    cli()
