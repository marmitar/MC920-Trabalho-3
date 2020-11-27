#include <stdint.h>
#include <stddef.h>
#include <math.h>
#include "ops.c"


typedef struct data {
    size_t tam;
    double param[4];
} data_t;



typedef double limiar_fn(const double vizinhanca[], size_t tam, data_t data);

static inline attribute(pure, nonnull)
double limiariza(const double *restrict buffer, size_t buflen, data_t data, limiar_fn *limiar) {
    size_t centro = (data.tam / 2) * (data.tam + 1);
    double pixel = buffer[centro];

    if (pixel > limiar(buffer, buflen, data)) {
        return 255.0;
    } else {
        return 0.0;
    }
}

#define LIMIARIZA(METODO) \
    extern attribute(pure, nonnull) \
    int limiariza_##METODO(const double *restrict buffer, intptr_t buflen, double *restrict retval, const data_t *restrict data) {\
        *retval = limiariza(buffer, (size_t) buflen, *data, limiar_##METODO); \
        return 1; \
    }


#define UNUSED attribute(unused)

static inline attribute(pure, nonnull)
double limiar_bernsen(const double vizinhanca[], size_t tam, UNUSED data_t data) {
    struct minmax z = minmax(vizinhanca, tam);

    return (z.min + z.max) / 2;
}
LIMIARIZA(bernsen)

static inline attribute(pure, nonnull)
double limiar_niblack(const double vizinhanca[], size_t tam, data_t data) {
    struct avgstd xy = avgstd(vizinhanca, tam);
    double k = data.param[0];

    return xy.mu + k * xy.sigma;
}
LIMIARIZA(niblack)

static inline attribute(pure, nonnull)
double limiar_sauvola(const double vizinhanca[], size_t tam, data_t data) {
    struct avgstd xy = avgstd(vizinhanca, tam);
    double k = data.param[0], R = data.param[1];

    return xy.mu * (1 + k * (xy.sigma / R - 1));
}
LIMIARIZA(sauvola)

static inline attribute(pure, nonnull)
double limiar_phansalskar(const double vizinhanca[], size_t tam, data_t data) {
    struct avgstd xy = avgstd(vizinhanca, tam);
    double k = data.param[0], R = data.param[1];
    double p = data.param[2], q = data.param[3];

    return xy.mu * (1 + p * exp(-q * xy.mu) + k * (xy.sigma / R - 1));
}
LIMIARIZA(phansalskar)

static inline attribute(pure, nonnull)
double limiar_contraste(const double vizinhanca[], size_t tam, data_t data) {
    size_t centro = (data.tam / 2) * (data.tam + 1);
    double pixel = vizinhanca[centro];

    struct minmax z = minmax(vizinhanca, tam);
    size_t dist_min = pixel - z.min;
    size_t dist_max = z.max - pixel;

    if (dist_min < dist_max) {
        return 255.0;
    } else {
        return 0.0;
    }
}
extern attribute(pure, nonnull) \
int limiariza_contraste(const double *restrict buffer, intptr_t buflen, double *restrict retval, const data_t *restrict data) {
    *retval = limiar_contraste(buffer, buflen, *data);
    return 1;
}

static inline attribute(pure, nonnull)
double limiar_media(const double vizinhanca[], size_t tam, UNUSED data_t data) {
    return mean(vizinhanca, tam);
}
LIMIARIZA(media)

static inline attribute(pure, nonnull)
double limiar_media(const double vizinhanca[], size_t tam, UNUSED data_t data) {
    return mean(vizinhanca, tam);
}
LIMIARIZA(media)
