#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
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

static attribute(nonnull)
size_t partition(double array[], size_t len) {
    double pivot = array[0];

    size_t lo = 1, hi = len-1;
    while (lo <= hi) {
        if (array[lo] <= pivot) {
            array[lo-1] = array[lo];
            lo++;
        } else {
            double tmp = array[hi];
            array[hi] = array[lo];
            array[lo] = tmp;
            hi--;
        }
    }

    array[hi] = pivot;
    return hi;
}

static attribute(pure, nonnull)
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
double median(double array[], size_t len) {
    size_t k1 = (len - 1) / 2;
    size_t k2 = len / 2;
    double m1 = -1.0, m2 = -1.0;

    size_t lo = 0;
    while (m1 < 0.0) {
        size_t q = lo + partition(array + lo, len - lo);
        if (q < k1) {
            lo = q + 1;
        } else if (q > k2) {
            len = q;
        } else {
            if (q == k1) {
                m1 = array[q];
            } else {
                m1 = dmax(array + lo, q - lo);
            }
            if (q == k2) {
                m2 = array[q];
            } else {
                m2 = dmin(array + q + 1, len - q - 1);
            }
        }
    }
    return (m1 + m2) / 2;
}
