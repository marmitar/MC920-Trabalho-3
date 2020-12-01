#!/bin/bash

mkdir -p resultados/base
for img in $(ls imagens)
do
    nome="${img%.*}"
    echo $img $nome
    convert imagens/$img resultados/base/$nome.png
done
