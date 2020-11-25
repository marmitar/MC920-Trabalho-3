from ctypes import Structure, CDLL, c_size_t, c_double, c_void_p, cast, pointer
from pathlib import Path
from scipy import LowLevelCallable


def compile(source: Path, out: Path) -> None:
    from subprocess import run

    CC = '/usr/bin/gcc'
    CFLAGS = [
        '-std=gnu11', '-shared', '-rdynamic',
        '-O3', '-ffast-math', '-march=native', '-mtune=native',
        '-DNDEBUG', '-Werror', '-Wall',
        '-Wpedantic', '-Wunused-result'
    ]
    PATH = [
        str(source.absolute()),
        '-o', str(out.absolute())
    ]
    run([CC, *CFLAGS, *PATH], check=True)


def load(lib: Path) -> CDLL:
    if not lib.exists():
        source = lib.with_suffix('.c')
        compile(source, lib)

    path = str(lib.absolute())
    return CDLL(path)


liblimiar = Path(__file__).with_suffix('.so')
liblimiar = load(liblimiar)


class UserData(Structure):
    _fields_ = [
        ("tam", c_size_t),
        ("param", c_double * 4)
    ]


def limiariza_fn(nome: str, tam: int, *params: float) -> LowLevelCallable:
    data = UserData(tam, *params)
    ptr = cast(pointer(data), c_void_p)

    sig = f"int limiariza_{nome}(const double *restrict buffer, intptr_t buflen, double *restrict retval, const void *restrict data)"
    fn = getattr(liblimiar, f'limiariza_{nome}')
    return LowLevelCallable(fn, ptr, sig)


def limiariza_bernsen(tam: int) -> LowLevelCallable:
    return limiariza_fn('bernsen', tam)
