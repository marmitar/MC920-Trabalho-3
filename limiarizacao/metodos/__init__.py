from scipy.ndimage import generic_filter
from locais import limiariza_fn
import numpy as np

from typing import Dict, Optional
from scipy import LowLevelCallable
from tipos import Image, Metodo



class MetodoGlobal(Metodo):
    def limiariza(self, img: Image, tam: int, L: Optional[float]=None) -> Image:
        if limite is None:
            limite = np.mean(img)

        min, max = np.uint8(0), np.uint8(255)
        return np.where(img > limite, max, min)

class MetodoLocal(Metodo):
    def __init__(self, name, **params: float):
        self.name = name
        self.params = params

    def fn(self, tam: int, params: Dict[str, float]) -> LowLevelCallable:
        args = []
        for k, v in self.params:
            v = params.get(k, v)
            args.append(v)

        return limiariza_fn(self.name, tam, *args)

    def limiariza(self, img: Image, tam: int, **params: float) -> Image:
        fn = self.fn(tam, params)
        size = 2 * tam + 1
        return generic_filter(img, fn, size=size)


METODO: Dict[str, Metodo] = {
    'global': MetodoGlobal('global'),
    'bernsen': MetodoLocal('bernsen')
}
