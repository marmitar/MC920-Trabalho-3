#include <stdint.h>
#include <stddef.h>
#include <math.h>


#define attribute(...) __attribute__((__VA_ARGS__))


struct minmax {
    double min, max;
};


static attribute(pure, nonnull)
struct minmax minmax(const double array[], size_t len) {
    double min, max;
    size_t start;

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

    for (size_t i = start; i < len; i += 2) {
        double menor = array[i];
        double maior = array[i+1];

        if (maior < menor) {
            menor = maior;
            maior = array[i];
        }

        if (menor < min) min = menor;
        if (maior > max) max = maior;
    }

    return (struct minmax) {.min = min, .max = max};
}

// static attribute(pure, nonnull)
// double mean(const double array[], size_t len) {
//     double sum = 0;
//     for (size_t i = 0; i < len; i++) {
//         sum += array[i];
//     }
//     return sum / len;
// }

struct avgstd {
    double mu, sigma;
};

static attribute(pure, nonnull)
struct avgstd avgstd(const double array[], size_t len) {
    double sum = 0, sumsq = 0;
    for (size_t i = 0; i < len; i++) {
        double val = array[i];
        sum += val;
        sumsq += val * val;
    }

    double avg = sum / len;
    double avgsq = sumsq / len;
    double std = sqrt(avgsq - avg * avg);

    return (struct avgstd) {.mu = avg, .sigma = std};
}
