# [JigsawGenerator](https://github.com/Bollos00/JigsawGenerator)

![Source to original image <https://commons.wikimedia.org/wiki/File:Gnu_wallpaper.png>](./examples/output_example.png)

## Introduction

This repository contains a simple rectangular [jigsaw](https://en.wikipedia.org/wiki/Jigsaw_puzzle) generator software written in python using the [Qt](https://en.wikipedia.org/wiki/Qt_%28software%29) Framework (with [PySide2](https://pypi.org/project/PySide2) or [PySide6](https://pypi.org/project/PySide6)) and [numpy](https://pypi.org/project/numpy/).

The image shown above contains a example of output generated from this software. The example shows a image of PNG format with the Jigsaw painted above the image. The formats JPG, GIF and BMP are also supported. It is also possible to generate an output on the SVG format, containing only the paths of the jigsaw.

## How to use it

First install the needed dependencies (PySide and numpy) the way you prefer. With pip it can be done with:
```sh
pip install pyside2 numpy
```

You can also use PySide6 if you prefer. If it is your case, on the file `jigsaw_generator/jigsaw_generator_info.py` change the value of the variable `PYSIDE_VERSION` to `'6'`.

Next generate the UI file:
```sh
pyside2-uic jigsaw_generator/jigsaw_generator_main_window.ui > jigsaw_generator/ui_jigsaw_generator_main_window.py
```

At least go to the `jigsaw_generator` directory and run the program:
```sh
cd jigsaw_generator
python main.py
```
