#!/bin/bash

mkdir -p resultados/base
mkdir -p resultados/hist
for img in $(ls imagens)
do
    nome="${img%.*}"
    echo $img $nome
    convert imagens/$img resultados/base/$nome.png
    python3 histograma.py imagens/$img resultados/hist/$nome.pgf
done
