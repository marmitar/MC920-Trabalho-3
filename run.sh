#!/bin/bash

echo -n Histogramas:
mkdir -p resultados/base
mkdir -p resultados/hist
for img in $(ls imagens)
do
    nome="${img%.*}"
    echo -n ' ' $nome
    # convert imagens/$img resultados/base/$nome.png
    # python3 histograma.py imagens/$img resultados/hist/$nome.pgf
done
echo

function run {
    argv=($@)
    python3 limiarizacao -o resultados/$1/$3.png \
        imagens/$2.pgm $1 ${argv[@]:3}
    echo $1 $3 ${argv[@]:3} $(python3 porcentagem.py resultados/$1/$3.png)
}

mkdir -p resultados/global
# run global retina retina -T 128
# run global wedge wedge100 -T 100
# run global wedge wedge110 -T 110

mkdir -p resultados/bernsen
# run bernsen baboon baboon -r 50
# run bernsen peppers peppers -r 50
# run bernsen wedge wedge -r 20
# run bernsen sonnet sonnet -r 20

mkdir -p resultados/niblack
# run niblack sonnet sonnet50 -r 50 -k -0.5
# run niblack sonnet sonnet20 -r 20 -k -0.5
# run niblack wedge wedge -r 50 -k -0.3
# run niblack fiducial fiducial -r 50 -k -0.5

mkdir -p resultados/sauvola
run sauvola sonnet sonnet -k 0.08 -R 100
run sauvola retina retina -k -0.5 -R 100
run sauvola wedge wedge -k 0.08 -R 200
run sauvola monarch monarch -k 0.5 -R 300
