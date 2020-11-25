#include <stdint.h>
#include <stddef.h>
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
        return 1.0;
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
