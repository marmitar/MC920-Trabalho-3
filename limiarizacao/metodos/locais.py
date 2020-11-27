from ctypes import Structure, CDLL, c_size_t, c_double, c_void_p, cast, pointer
from pathlib import Path
from typing import Tuple
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

def libname() -> Tuple[Path, Path]:
    source = Path(__file__).with_suffix('.c')
    lib = source.parent / f'lib{source.name}'
    lib = lib.with_suffix('.so')
    return lib, source

def load() -> CDLL:
    lib, source = libname()

    if not lib.exists():
        compile(source, lib)

    path = str(lib.absolute())
    return CDLL(path)

liblimiar = load()


class UserData(Structure):
    _fields_ = [("param", c_double * 4)]


def limiariza_fn(nome: str, *params: float) -> LowLevelCallable:
    data = UserData(*params)
    ptr = cast(pointer(data), c_void_p)

    fn = getattr(liblimiar, f'limiariza_{nome}')
    sig = "int (double *, intptr_t, double *, void *)"
    return LowLevelCallable(fn, ptr, sig)
