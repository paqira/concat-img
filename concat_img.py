from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from os import PathLike

import click
from PIL import Image

__version__ = "0.0.1"


@contextmanager
def context():
    try:
        yield
    except Exception as e:  # noqa: BLE001
        ctx = click.get_current_context()
        ctx.fail(str(e))


def get_size(shape: tuple[int, int], files: Sequence[PathLike]) -> tuple[int, int]:
    hs, vs = shape

    # calc figure size
    width, height = 0, 0
    for v in range(vs):
        _width, _height = 0, 0
        for h in range(hs):
            with context():
                img = Image.open(files[v * hs + h])

            _width += img.width
            _height = max(_height, img.height)
        width = max(width, _width)
        height += _height

    return width, height


@click.command()
@click.argument("shape", type=(int, int))
@click.argument("out", metavar="OUT_NAME", type=click.Path())
@click.argument("file", nargs=-1, type=click.Path(exists=True, dir_okay=False))
@click.version_option(__version__)
def main(shape: tuple[int, int], out: PathLike, file: Sequence[PathLike]):
    """Concatenates/Tiling images

    It aligns FILEs as SHAPE tile.

    SHAPE is a pair of integer, horizontal and vertical tile length.
    OUT_NAME is a resulting image file name.
    FILE is source images.

    concat-img 3 2 result.jpg src.0.jpg src.1.jpg src.2.jpg src.3.jpg src.4.jpg src.5.jpg

    results an image that aligns the input files as below:

    \b
    +---+---+---+
    | 0 | 1 | 2 |
    +---+---+---+
    | 3 | 4 | 5 |
    +---+---+---+
    """
    # print help if no file given
    if not file:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    # check size
    hs, vs = shape
    if hs * vs != len(file):
        ctx = click.get_current_context()
        ctx.fail(f"Invalid Shape: expected h * v = {len(file)}, got {hs} * {vs}.")

    # destination image
    dst = Image.new("RGB", size=get_size(shape, file))

    # concat
    v_offset = 0
    for v in range(vs):
        h_offset = 0
        _v_offset = 0
        for h in range(hs):
            with context():
                img = Image.open(file[v * hs + h])

            dst.paste(img, (h_offset, v_offset))
            h_offset += img.width
            _v_offset = max(_v_offset, img.height)
        v_offset += _v_offset

    with context():
        dst.save(out)


if __name__ == "__main__":
    main()
