/**
 * Operações auxiliares para as funções de limiarização.
 */
#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// atributos do GCC
#define attribute(...) \
    __attribute__((__VA_ARGS__))


// Saída com o mínimo e o máximo de um vetor.
struct minmax {
    double min, max;
};

static attribute(pure, nonnull)
/**
 * Encontra o mínimo e o máximo de um vetor.
 */
struct minmax minmax(const double array[], size_t len) {
    double min, max;
    size_t start;

    // seleciona o mín e máx dos iniciais
    if (len % 2 == 1) {
        min = max = array[0];
        start = 1;
    } else if (array[0] < array[1]) {
        min = array[0];
        max = array[1];
        start = 2;
    } else {
        min = array[1];
        max = array[0];
        start = 2;
    }
    // para que reste um número para de elementos
    for (size_t i = start; i < len; i += 2) {
        // que são analisados par a par
        double menor = array[i];
        double maior = array[i+1];

        if (maior < menor) {
            menor = maior;
            maior = array[i];
        }

        if (menor < min) min = menor;
        if (maior > max) max = maior;
    }
    // retorno na struct specífica
    return (struct minmax) {.min = min, .max = max};
}

static attribute(pure, nonnull)
/**
 * Cálculo da média do vetor.
 */
double mean(const double array[], size_t len) {
    double sum = 0;
    for (size_t i = 0; i < len; i++) {
        sum += array[i];
    }
    return sum / len;
}

// Saída com a média e desv.pad. do vetor.
struct avgstd {
    double mu, sigma;
};

static attribute(pure, nonnull)
/**
 * Encontra média e desvio padrão simultaneamente.
 */
struct avgstd avgstd(const double array[], size_t len) {
    // soma e soma dos quadrados
    double sum = 0, sumsq = 0;
    for (size_t i = 0; i < len; i++) {
        double val = array[i];
        sum += val;
        sumsq += val * val;
    }

    // média
    double avg = sum / len;
    // desvio padrão
    double avgsq = sumsq / len;
    double std = sqrt(avgsq - avg * avg);
    // retorno na struct specífica
    return (struct avgstd) {.mu = avg, .sigma = std};
}

static attribute(nonnull)
/**
 * Particionamento para encontrar
 */
size_t partition(double array[], size_t len) {
    // pivô como elemento na posição média
    double pivot = array[len / 2];
    array[len / 2] = array[0];

    size_t lo = 1, hi = len-1;
    while (lo <= hi) {
        // move os elementos menores para
        // as posições iniciais
        if (array[lo] <= pivot) {
            array[lo-1] = array[lo];
            lo++;
        // e os maiores para o final
        } else {
            double tmp = array[hi];
            array[hi] = array[lo];
            array[lo] = tmp;
            hi--;
        }
    }
    // guarda o pivo na sua posição correta
    array[hi] = pivot;
    return hi;
}

static attribute(pure, nonnull)
/**
 * Encontra o mínimo do vetor.
 */
double dmin(const double array[], size_t len) {
    double min = array[0];
    for (size_t i = 1; i < len; i++) {
        if (array[i] < min) {
            min = array[i];
        }
    }
    return min;
}

static attribute(pure, nonnull)
/**
 * Encontra o máximo do vetor.
 */
double dmax(const double array[], size_t len) {
    double max = array[0];
    for (size_t i = 1; i < len; i++) {
        if (array[i] > max) {
            max = array[i];
        }
    }
    return max;
}

static attribute(nonnull)
/**
 * Encontra a mediana de um vetor positivo.
 */
double median(const double input[], size_t len) {
    // copia o vetor para o heap
    double *array = alloca(len * sizeof(double));
    memcpy(array, input, len * sizeof(double));

    // posição das medianas
    size_t k1 = (len - 1) / 2;
    size_t k2 = len / 2;
    // valores das medianas (negativo deve ser inválido)
    double m1 = -1.0, m2 = -1.0;

    size_t lo = 0;
    // a mediana real será positiva
    while (m1 < 0.0) {
        // posição resultado do particionamento
        size_t q = lo + partition(array + lo, len - lo);
        // se menor, busca nos maiores
        if (q < k1) {
            lo = q + 1;
        // se maior, busca nos menores
        } else if (q > k2) {
            len = q;
        // então é alguma das medianas
        } else {
            // se for a menor, marca ela
            if (q == k1) {
                m1 = array[q];
            // senão busca o maior dos menores
            } else {
                m1 = dmax(array + lo, q - lo);
            }
            // se for a maior, marca ela
            if (q == k2) {
                m2 = array[q];
            // senão busca a menor das maiores
            } else {
                m2 = dmin(array + q + 1, len - q - 1);
            }
        }
    }
    // média das medianas
    return (m1 + m2) / 2;
}
