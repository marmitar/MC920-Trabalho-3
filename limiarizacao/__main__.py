import sys
from argparse import ArgumentParser, ArgumentTypeError
from inout import imgread, imgwrite, imgshow
from metodos import METODO


# parser de argumentos
description = 'Ferramenta de aplicação de meios-tons para o Trabalho 2.'
usage = '%(prog)s [OPTIONS] INPUT'

parser = ArgumentParser(description=description, allow_abbrev=False)
# argumentos necessários
parser.add_argument('input', metavar='INPUT', type=str,
                    help='imagem de entrada')
subparsers = parser.add_subparsers(required=True,
                    help='método de limiarização')
# opções de saída
optsaida = parser.add_argument_group('opções de saída')
optsaida.add_argument('-o', '--output', type=str, action='append', metavar='FILE',
                    help='arquivo para gravar o resultado')
optsaida.add_argument('-f', '--force-show', action='store_true',
                    help='sempre mostra o resultado final em uma janela')


def add_subparser(nome: str, descricao: str) -> ArgumentParser:
    return subparsers.add_parser(nome, description=descricao)

for metodo in METODO.values():
    metodo.add_arg_parser(add_subparser)

if __name__ == "__main__":
    args = parser.parse_args()

    # entrada
    arquivo = args.input
    img = imgread(arquivo)

    # aplica pontilhado
    img = args.metodo.limiariza(img, args)
    # range completo para a visualização
    img *= 255

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
