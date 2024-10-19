# concat-img

CLI that concatenates images.

It aligns FILEs as SHAPE tile.

## Installation

```shell
pipx install git+https://github.com/paqira/concat-img
```

## Usage

```shell
concat-img 3 2 result.jpg src.0.jpg src.1.jpg src.2.jpg src.3.jpg src.4.jpg src.5.jpg
```

results an image that aligns the input files as below:

```text
+---+---+---+
| 0 | 1 | 2 |
+---+---+---+
| 3 | 4 | 5 |
+---+---+---+
```

## Licence

MIT
