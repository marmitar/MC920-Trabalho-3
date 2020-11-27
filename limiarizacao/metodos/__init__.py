from enum import Enum, unique
from typing import Dict, Callable, Optional
from scipy import LowLevelCallable
from scipy.ndimage import generic_filter
import numpy as np

from locais import limiariza_bernsen
from tipos import Image



Params = Dict[str, float]
Metodo = Callable[[int, ...], LowLevelCallable]

METODO: Dict[str, Optional[Metodo]] = {
    'global': None,
    'bernsen': limiariza_bernsen
}

def limiariza(img: Image, tam: int, metodo: str, params: Params) -> Image:
    fn = METODO[metodo]
    if fn is None:
        return limiariza_global(img, **params)
    else:
        size = 2 * tam + 1
        return generic_filter(img, fn(tam, **params), size=size)


def limiariza_global(img: Image, L: Optional[float]=None) -> Image:
    if limite is None:
        limite = np.mean(img)

    min = np.uint8(0)
    max = np.uint8(255)
    return np.where(img > limite, max, min)
