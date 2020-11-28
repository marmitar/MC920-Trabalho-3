"""
Acesso das funções de limiarização em C.
"""
from ctypes import Structure, CDLL, c_size_t, c_double, c_void_p, cast, pointer
from pathlib import Path
from typing import Tuple
from scipy import LowLevelCallable


def compile(source: Path, out: Path) -> None:
    """
    Compila um arquivo fonte em C para uma biblioteca
    compartilhada (arquivo .so).
    """
    from subprocess import run

    CC = '/usr/bin/gcc'
    CFLAGS = [
        # flags necessárias
        '-std=gnu11', '-shared', '-rdynamic',
        # otimizações
        '-O3', '-ffast-math', '-march=native', '-mtune=native',
        # checagem de erros
        '-DNDEBUG', '-Werror', '-Wall', '-Wpedantic', '-Wunused-result'
    ]
    # entrada e saída do GCC
    PATH = [str(source.absolute()), '-o', str(out.absolute())]
    # chama GCC para a compilação
    run([CC, *CFLAGS, *PATH], check=True)

def libname() -> Tuple[Path, Path]:
    """
    Caminho da blibioteca (liblocais.so) e do arquivo fonte (locais.c).
    """
    source = Path(__file__).with_suffix('.c')
    lib = source.parent / f'lib{source.name}'
    lib = lib.with_suffix('.so')
    return lib, source

def load() -> CDLL:
    """
    Carrega a bibliteca (liblocais.so), utilizando o caminho certo.
    """
    lib, source = libname()

    # compila se necessário
    if not lib.exists():
        compile(source, lib)

    path = str(lib.absolute())
    return CDLL(path)

# biblioteca em C
liblimiar = load()


class UserData(Structure):
    """
    Estrutura com os parâmetros da limiarização.
    """
    _fields_ = [("param", c_double * 4)]


def limiariza_fn(nome: str, *p: float) -> LowLevelCallable:
    """
    Monta a função de limiarização local para o `scipy`. A função deve ser
    "limiariza_[NOME]", onde [NOME] é o parâmetro da entrada padrão.
    Recebe também os parâmetros da limiarização.
    """
    array = c_double * 4
    data = UserData(array(*p))
    ptr = cast(pointer(data), c_void_p)

    fn = getattr(liblimiar, f'limiariza_{nome}')
    sig = "int (double *, intptr_t, double *, void *)"
    return LowLevelCallable(fn, ptr, sig)
