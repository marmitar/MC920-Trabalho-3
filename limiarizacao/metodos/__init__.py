from argparse import ArgumentTypeError
from scipy.ndimage import generic_filter
from .locais import limiariza_fn
import numpy as np

from typing import List, Optional
from scipy import LowLevelCallable
from tipos import Image, Metodo, AddSubParser, Namespace



class MetodoGlobal(Metodo):
    def limiariza(self, img: Image, params: Namespace) -> Image:
        limite = params.T
        if limite is None:
            limite = np.mean(img)

        min, max = np.uint8(0), np.uint8(255)
        return np.where(img > limite, max, min)

    def add_arg_parser(self, parser: AddSubParser) -> None:
        subparser = parser('global', 'Método Global.')
        subparser.add_argument('-T', metavar='num', type=float,
            help='Limiar fixo. Usa a intensidade média da imagem, se não for definido.')
        subparser.set_defaults(metodo=self)


def tamanho(entrada: str) -> int:
    try:
        tam = int(entrada, base=10)
        if tam < 3 or tam % 2 != 1:
            raise ValueError()
        return tam
    except ValueError:
        raise ArgumentTypeError(f'tamanho inválido: {entrada}')


class MetodoLocal(Metodo):
    def __init__(self, name: str, description: str, **params: float):
        self.name = name
        self.description = description
        self.params = params

    def fn(self, params: Namespace) -> LowLevelCallable:
        args = []
        for key, default in self.params.items():
            value = getattr(params, key, None)
            if value is None:
                args.append(default)
            else:
                args.append(value)

        return limiariza_fn(self.name, *args)

    def limiariza(self, img: Image, params: Namespace) -> Image:
        fn = self.fn(params)
        return generic_filter(img, fn, size=params.tamanho, mode='mirror')

    def add_arg_parser(self, parser: AddSubParser) -> None:
        subparser = parser(self.name, self.description)
        subparser.add_argument('-t', '--tamanho', metavar='num', type=tamanho, default=5,
            help='tamanho da vizinhança de limiarização (default=5)')

        if self.params:
            params = subparser.add_argument_group('parâmetros')
        for key, default in self.params.items():
            params.add_argument(f'-{key}', type=float, default=default,
                                help=f'(default = {default})')
        subparser.set_defaults(metodo=self)

class MetodoNormalizado(MetodoLocal):
    def limiariza(self, img: Image, params: Namespace) -> Image:
        resultado = super().limiariza(img / 255, params)
        min, max = np.uint8(0), np.uint8(255)
        return np.where(resultado < 1, min, max)

METODOS: List[Metodo] = {
    MetodoGlobal(),
    MetodoLocal('bernsen', 'Método de Bernsen.'),
    MetodoLocal('niblack', 'Método de Niblack.', k=0.5),
    MetodoLocal('sauvola', 'Método de Sauvola e Pietaksinen.', k=0.5, R=128),
    MetodoNormalizado('phansalskar', 'Método de Phansalskar, More e Sabale.', k=0.25, R=0.5, p=2, q=10),
    MetodoLocal('contraste', 'Método do Contraste.'),
    MetodoLocal('media', 'Método da Média.'),
    MetodoLocal('mediana', 'Método da Mediana.')
}
