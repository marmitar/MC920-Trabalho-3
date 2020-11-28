"""
Tratamento geral dos argumentos da linha de comando.
"""
import sys
from argparse import ArgumentParser, ArgumentTypeError
from inout import imgread, imgwrite, imgshow
from metodos import METODOS


# parser de argumentos
parser = ArgumentParser(allow_abbrev=False,
                        description='Ferramenta de limiarização para o Trabalho 3.')
# argumentos necessários
parser.add_argument('input', metavar='INPUT', type=str,
                    help='imagem de entrada')
subparsers = parser.add_subparsers(help='método de limiarização')
# opções de saída
optsaida = parser.add_argument_group('opções de saída')
optsaida.add_argument('-o', '--output', type=str, action='append', metavar='FILE',
                    help='arquivo para gravar o resultado')
optsaida.add_argument('-f', '--force-show', action='store_true',
                    help='sempre mostra o resultado final em uma janela')


def add_subparser(nome: str, descricao: str) -> ArgumentParser:
    """
    Adiciona um subparser na linha de comando.
    """
    return subparsers.add_parser(nome, description=descricao)

for metodo in METODOS:
    # adiciona o parser de cada método
    metodo.add_arg_parser(add_subparser)


if __name__ == "__main__":
    args = parser.parse_args()

    # entrada
    arquivo = args.input
    img = imgread(arquivo)

    # aplica limiarização
    img = args.metodo.limiariza(img, args)

    # saída
    if args.output:
        for output in args.output:
            try:
                imgwrite(img, output)
            # em caso de erro, mostra o erro
            # mas continua a execução
            except ValueError as err:
                print(err, file=sys.stderr)

    if args.output is None or args.force_show:
        imgshow(img, arquivo)
