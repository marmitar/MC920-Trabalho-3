#include <stdint.h>
#include <stddef.h>
#include <math.h>


#define attribute(...) __attribute__((__VA_ARGS__))


struct argminmax {
    size_t min, max;
};

static attribute(pure, nonnull)
struct argminmax argminmax(const double array[], size_t len) {
    double min, max;
    size_t idmin, idmax;
    size_t start;

    if (len % 2 == 1) {
        idmin = idmax = 0;
        start = 1;
    } else if (array[0] < array[1]) {
        idmin = 0;
        idmax = 1;
        start = 2;
    } else {
        idmin = 1;
        idmax = 0;
        start = 2;
    }

    min = array[idmin];
    max = array[idmax];
    for (size_t i = start; i < len; i += 2) {
        size_t menor = i;
        size_t maior = i+1;

        if (array[maior] < array[menor]) {
            menor = i+1;
            maior = i;
        }

        if (array[menor] < min) {
            min = array[menor];
            idmin = menor;
        }
        if (maior > max) {
            max = array[maior];
            idmax = maior;
        }
    }

    return (struct argminmax) {.min = idmin, .max = idmax};
}

struct minmax {
    double min, max;
};

static attribute(pure, nonnull)
struct minmax minmax(const double array[], size_t len) {
    struct argminmax id = argminmax(array, len);

    return (struct minmax) {.min = array[id.min], .max = array[id.max]};
}

static attribute(pure, nonnull)
double mean(const double array[], size_t len) {
    double sum = 0;
    for (size_t i = 0; i < len; i++) {
        sum += array[i];
    }
    return sum / len;
}

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
