import json
import logging
import os
import sys

from marshmallow import fields
from marshmallow import INCLUDE
from marshmallow import Schema
from marshmallow import ValidationError
from rich.logging import RichHandler

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


FORMAT = "%(message)s"
logging.basicConfig(
    level=LOG_LEVEL, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


class LinkSchema(Schema):
    url = fields.URL(required=True)
    title = fields.Str(required=True)


class GeneratorSchema(Schema):
    tag = fields.Str(required=True, default="week note")
    output = fields.Str(required=True, default="~/weeknotes/")


class ConfigSchema(Schema):
    feeds = fields.List(fields.Nested(LinkSchema), required=True)
    fix_links = fields.List(fields.Nested(LinkSchema), required=True)
    generator = fields.Nested(GeneratorSchema, required=True)

    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE


def get_config_schema(file_path: str) -> ConfigSchema:
    with open(file_path) as file:
        data = json.load(file)
    try:
        return ConfigSchema().load(data)
    except ValidationError as error:
        log.error(f"ERROR: {file_path} is invalid")
        log.error(error.messages)
        sys.exit(1)
