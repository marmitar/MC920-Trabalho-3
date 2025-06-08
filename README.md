# Image Processing (MC920) - Thresholding

- [Requirements](papers/enunciado.pdf)
- [Report](papers/entrega.pdf)

This project implements a variety of global and local thresholding techniques to binarize grayscale images. A simple Python CLI applies each method to a PGM input, producing a two-tone output and performance metrics.

The implemented methods are:

- Global threshold
- Bernsen
- Niblack
- Sauvola & Pietaksinen
- Phansalskar, More & Sabale
- Contrast
- Local mean
- Local median

Only the global method is written in pure NumPy; all local algorithms are implemented in C and exposed via FFI for speed.

![Sauvola and Pietaksinen thresholding method applied on "Sonnet for Lena"](resultados/sauvola/sonnet.png "Sauvola and Pietaksinen")
