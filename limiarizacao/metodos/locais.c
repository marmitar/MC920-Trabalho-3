/**
 * Funções de limiarização em uma vizinhança.
 */
#include <stdint.h>
#include <stddef.h>
#include <math.h>
#include "ops.c"

// Parâmetros da limiarização.
typedef struct data {
    double param[4];
} data_t;


// Tipo de função que calcula o limiar de uma vizinhança.
typedef double limiar_fn(const double vizinhanca[], size_t tam, data_t data);

static inline attribute(pure, nonnull)
/**
 * Encontra o limiar da vizinhança e aplica de acordo
 * com o pixel central.
 */
double limiariza(const double *restrict buffer, size_t buflen, data_t data, limiar_fn *limiar) {
    // pixel central
    double pixel = buffer[buflen / 2];

    // aplica de acordo com uma função de limiar da região.
    if (pixel > limiar(buffer, buflen, data)) {
        return 255.0;
    } else {
        return 0.0;
    }
}

// Macro que gera a função de limiarização a ser exportada, com
// as entradas e saídas necessárias.
#define LIMIARIZA(METODO) \
    extern attribute(pure, nonnull) \
    int limiariza_##METODO(const double *restrict buffer, intptr_t buflen, double *restrict retval, const data_t *restrict data) {\
        *retval = limiariza(buffer, (size_t) buflen, *data, limiar_##METODO); \
        return 1; \
    }


// Marcador de parâmetro não utilizado na função.
#define UNUSED attribute(unused)

static inline attribute(pure, nonnull)
/**
 * Método de Bernsen.
 */
double limiar_bernsen(const double vizinhanca[], size_t tam, UNUSED data_t data) {
    struct minmax z = minmax(vizinhanca, tam);

    return (z.min + z.max) / 2;
}
LIMIARIZA(bernsen)

static inline attribute(pure, nonnull)
/**
 * Método de Niblack.
 */
double limiar_niblack(const double vizinhanca[], size_t tam, data_t data) {
    struct avgstd xy = avgstd(vizinhanca, tam);
    double k = data.param[0];

    return xy.mu + k * xy.sigma;
}
LIMIARIZA(niblack)

static inline attribute(pure, nonnull)
/**
 * Método de Sauvola e Pietaksinen.
 */
double limiar_sauvola(const double vizinhanca[], size_t tam, data_t data) {
    struct avgstd xy = avgstd(vizinhanca, tam);
    double k = data.param[0], R = data.param[1];

    return xy.mu * (1.0 + k * ((xy.sigma / R) - 1.0));
}
LIMIARIZA(sauvola)

static inline attribute(pure, nonnull)
/**
 * Método de Phansalskar, More e Sabale.
 */
double limiar_phansalkar(const double vizinhanca[], size_t tam, data_t data) {
    struct avgstd xy = avgstd(vizinhanca, tam);
    double k = data.param[0], R = data.param[1];
    double p = data.param[2], q = data.param[3];

    return xy.mu * (1.0 + p * exp(-q * xy.mu) + k * ((xy.sigma / R) - 1.0));
}
LIMIARIZA(phansalkar)

static inline attribute(pure, nonnull)
/**
 * Método do Contraste.
 */
double limiar_contraste(const double vizinhanca[], size_t tam) {
    double pixel = vizinhanca[tam / 2];

    struct minmax z = minmax(vizinhanca, tam);
    // proximidade do mínimo da vizinhança
    size_t dist_min = pixel - z.min;
    // proximidade do máximo
    size_t dist_max = z.max - pixel;

    // retorna o pixel, em vez do limite
    if (dist_min < dist_max) {
        return 255.0;
    } else {
        return 0.0;
    }
}
extern attribute(pure, nonnull)
// Função especial de limiarização do contraste.
int limiariza_contraste(const double *restrict buffer, intptr_t buflen, double *restrict retval, UNUSED const data_t *_data) {
    *retval = limiar_contraste(buffer, (size_t) buflen);
    return 1;
}

static inline attribute(pure, nonnull)
/**
 * Método da Média.
 */
double limiar_media(const double vizinhanca[], size_t tam, UNUSED data_t data) {
    return mean(vizinhanca, tam);
}
LIMIARIZA(media)

static inline attribute(pure, nonnull)
/**
 * Método da Mediana.
 */
double limiar_mediana(const double vizinhanca[], size_t tam, UNUSED data_t data) {
    return median(vizinhanca, tam);
}
LIMIARIZA(mediana)
