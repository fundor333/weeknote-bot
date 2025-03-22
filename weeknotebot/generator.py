import datetime
import logging
import os
from pathlib import Path

from rich.logging import RichHandler

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


FORMAT = "%(message)s"
logging.basicConfig(
    level=LOG_LEVEL, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


WEEKNOTE_TEMPLATE = """---
title: "Week Note Nº {week}/{year}"
date: "{today_str}"
lastmod: "{today_str}"
draft: true
tags: ["{tag}"]
summary: "Random notes for week {week} of {year}"
---

"""


def get_data_meta(today) -> tuple[str, str, str]:
    year = today.strftime("%Y")
    week = today.strftime("%W")
    today_str = today.strftime("%Y-%m-%d")
    return year, week, today_str


def generate_weeknote(config: dict, today: datetime) -> tuple[str, str]:
    year, week, today_str = get_data_meta(today)
    weeknote = WEEKNOTE_TEMPLATE.format(
        week=week,
        year=year,
        today_str=today_str,
        tag=config["generator"]["tag"],
    )
    file_name = f"{year}/{week}.md"
    log.debug(file_name)
    log.debug(weeknote)
    return weeknote, file_name


def write_weeknote(config: dict, today: datetime) -> None:
    weeknote, filename = generate_weeknote(config, today)
    output = os.path.join(config["generator"]["output"], filename)

    output_file = Path(output)
    output_file.parent.mkdir(exist_ok=True, parents=True)

    with open(output_file, "w") as f:
        f.write(weeknote)
