from dataclasses import Field

import pytest

from cliappatra.core import create_app
from cliappatra.models import Field


class TestCliappatra:
    def test_cli(self):
        def main(
                name: str = Field(help="name of the person to greet"),
                /,
                debug: bool = Field(help="enable debug"),
        ):
            pass

        app = create_app(
            prog="hello",
            description="A CLI app that says hello",
            epilog="for testing purposes only",
            version="0.1.0",
            parser=main,
        )
        # tree = {cliopatra: {pharaoh: None}}

        print(app.parse_args(["-h"]))
        # print(app.parse_args(["-v"]))
        assert False
