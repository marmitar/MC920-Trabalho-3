"""
Métodos de Limiarização, Global e Local.
"""
from argparse import ArgumentTypeError, Namespace
from scipy.ndimage import generic_filter
from .locais import limiariza_fn
import numpy as np

from typing import List, Optional
from scipy import LowLevelCallable
from tipos import Image, Metodo, AddSubParser


class MetodoGlobal(Metodo):
    """
    Método de Limiarização Global.

    Recebe o parâmetro `T` da linha de comando. Se nada for recebido
    (ie. `T` é `None`) então usa a média da imagem como limite.
    """
    def limiariza(self, img: Image, params: Namespace) -> Image:
        """
        Aplica a limiarização em uma imagem.
        """
        limite = params.T
        if limite is None:
            limite = np.mean(img)

        # força saída como uint8
        obj, fundo = np.uint8(0), np.uint8(255)
        res: Image = np.where(img > limite, obj, fundo)
        return res

    def add_arg_parser(self, parser: AddSubParser) -> None:
        """
        Adiciona parser de argumentos do método com subparser
        para a linha de comandos.
        """
        subparser = parser('global', 'Método Global.')
        subparser.add_argument('-T', metavar='NUM', type=float,
            help='Limiar fixo. Usa a intensidade média da imagem, se não for definido.')
        subparser.set_defaults(metodo=self)


def raio(entrada: str) -> int:
    """
    Validade do raio da vizanhança (ou `(block size - 1) / 2`).

    Raio deve ser um inteiro positivo.
    """
    try:
        raio = int(entrada, base=10)
        if raio < 1:
            raise ValueError()
        return raio
    except ValueError:
        raise ArgumentTypeError(f'raio inválido: {entrada}')

def vizinhanca4(raio: int) -> np.ndarray:
    """
    Matriz booleana com a vizinhança-4 do pixel.
    """
    v = np.abs(np.arange(-raio, raio + 1))
    i, j = np.meshgrid(v, v)
    return i + j <= raio


class MetodoLocal(Metodo):
    """
    Métodos de Limiarização Local.

    Os parâmetros devem ser passados como argumentos com nome,
    sendo no máximo quatro (4) parâmetros.

    O nome e a descrição são usados para os argumentos da linha de
    comando. Além disso, o nome é usado para a chamada da função
    em C.
    """
    def __init__(self, name: str, description: str, **params: float):
        self.name = name
        self.description = description
        self.params = params

    def fn(self, params: Namespace) -> LowLevelCallable:
        """
        Recupera a função em C do método com os parâmetros
        corretos para a `scipy.ndimage.generic_filter`.
        """
        # argumentos devem ser passados na ordem que são definidos
        args = []
        for key, default in self.params.items():
            value = getattr(params, key, None)
            if value is None:
                args.append(default)
            else:
                args.append(value)

        return limiariza_fn(self.name, *args)

    def limiariza(self, img: Image, params: Namespace) -> Image:
        """
        Aplica a limiarização em uma imagem.
        """
        fn = self.fn(params)
        if params.viz4:
            tamanho = 2 * params.raio + 1
            res: Image = generic_filter(img, fn, size=tamanho, mode='mirror')
        else:
            viz = vizinhanca4(params.raio)
            res = generic_filter(img, fn, footprint=viz, mode='mirror')
        return res

    def add_arg_parser(self, parser: AddSubParser) -> None:
        """
        Adiciona parser de argumentos do método com subparser
        para a linha de comandos.
        """
        subparser = parser(self.name, self.description)
        # argumentos gerais do método
        subparser.add_argument('-r', '--raio', metavar='RAIO', type=raio, default=5,
            help='raio da vizinhança de limiarização (default=5)')
        subparser.add_argument('-v4', '--vizinhanca-4', dest='viz4', action='store_true',
            help='usa vizinhança-4 em vez de 8')

        # adiciona os parâmetros na linha de comando
        if self.params:
            params = subparser.add_argument_group('parâmetros')
        for key, default in self.params.items():
            params.add_argument(f'-{key}', metavar=key, type=float, default=default,
                                help=f'(default = {default})')
        subparser.set_defaults(metodo=self)

class MetodoNormalizado(MetodoLocal):
    """
    Métodos de Limiarização Local com Imagem Normalizada.

    A imagem é normalizado para o intervalo [0, 1] antes
    da limiarização.
    """
    def limiariza(self, img: Image, params: Namespace) -> Image:
        res: img = super().limiariza(img / 255, params).astype(np.uint8)
        return res


"""
Lista de métodos de limiarização com os parâmetros padrão de cada um.
"""
METODOS: List[Metodo] = [
    MetodoGlobal(),
    MetodoLocal('bernsen', 'Método de Bernsen.'),
    MetodoLocal('niblack', 'Método de Niblack.', k=0.5),
    MetodoLocal('sauvola', 'Método de Sauvola e Pietaksinen.', k=0.5, R=128),
    MetodoNormalizado('phansalkar', 'Método de Phansalkar, More e Sabale.', k=0.25, R=0.5, p=2, q=10),
    MetodoLocal('contraste', 'Método do Contraste.'),
    MetodoLocal('media', 'Método da Média.'),
    MetodoLocal('mediana', 'Método da Mediana.')
]
