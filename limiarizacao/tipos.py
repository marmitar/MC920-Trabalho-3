"""
Procolos para tipagem estática com ``mypy``.
"""
# from __future__ import annotations
from argparse import ArgumentParser, Namespace
from numpy import ndarray, uint8, float32
from typing import (
    TYPE_CHECKING, overload,
    Type, Union, Tuple, Callable
)

if TYPE_CHECKING:
    # Python 3.8+
    from typing import Literal, Protocol
else:
    from collections import defaultdict
    # Python 3.7-
    Literal = defaultdict(str)
    Protocol = object
    Image = 'Image'


"""
Função que adiciona subparser no ArgumentParser global do
programa. Recebe o título e a descrição do novo subparser.
"""
AddSubParser = Callable[[str, str], ArgumentParser]


class Metodo(Protocol):
    """
    Métodos de Limiarização.
    """
    def limiariza(self, img: Image, params: Namespace) -> Image:
        """
        Aplica a limiarização em uma imagem.

        Parâmetros
        ----------
        img: np.ndarray
            Matriz representando uma imagem.
        params: Namespace
            Argumentos parseados da linha de comando.

        Retorno
        -------
        out: np.ndarray
            Imagem limiarizada.
        """
        ...

    def add_arg_parser(self, parser: AddSubParser) -> None:
        """
        Adiciona parser de argumentos do método com subparser
        para a linha de comandos.

        Parâmetros
        ----------
        img: np.ndarray
            Matriz representando uma imagem.
        params: Namespace
            Argumentos parseados da linha de comando.

        Retorno
        -------
        out: np.ndarray
            Imagem limiarizada.
        """
        ...

class Image(ndarray): # type: ignore # pylint: disable=function-redefined
    """
    Matrizes que representam imagens em OpenCV e bibliotecas similares.
    """
    dtype: Type[uint8] = uint8
    ndim: Literal[2] = 2
    shape: Tuple[int, int]

    def copy(self) -> Image:
        ...

    @overload
    def __add__(self, other: Union[Image, int]) -> Image: ...
    @overload
    def __add__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __add__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    @overload
    def __sub__(self, other: Union[Image, int]) -> Image: ...
    @overload
    def __sub__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __sub__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    def __neg__(self) -> Image:
        ...

    def __pos__(self) -> Image:
        ...

    def __abs__(self) -> Image:
        ...

    def __invert__(self) -> Image:
        ...

    @overload
    def __mul__(self, other: Union[Image, int]) -> Image: ...
    @overload
    def __mul__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __mul__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    def __matmul__(self, other: ndarray) -> ndarray:
        ...

    @overload
    def __pow__(self, other: Union[Image, int]) -> Image: ...
    @overload
    def __pow__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __pow__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    @overload
    def __floordiv__(self, other: Union[Image, int]) -> Image: ...
    @overload
    def __floordiv__(self, other: ndarray) -> ndarray: ...
    def __floordiv__(self, other: Union[ndarray, int]) -> ndarray:
        ...

    def __truediv__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    @overload
    def __mod__(self, other: Union[Image, int]) -> Image: ...
    @overload
    def __mod__(self, other: Union[ndarray, float]) -> ndarray: ...
    def __mod__(self, other: Union[ndarray, float]) -> ndarray:
        ...

    def __rshift__(self, other: Union[Image, int]) -> Image:
        ...

    def __lshift__(self, other: Union[Image, int]) -> Image:
        ...

    def __and__(self, other: Union[Image, int]) -> Image:
        ...

    def __xor__(self, other: Union[Image, int]) -> Image:
        ...

    def __or__(self, other: Union[Image, int]) -> Image:
        ...
