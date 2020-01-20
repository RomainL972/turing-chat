#ifndef RSA_H_LEBBADI
#define RSA_H_LEBBADI

#include <gmpxx.h>
#include <vector>

std::vector<mpz_class> generateKeys(int size);
mpz_class crypt(mpz_class number, mpz_class exp, mpz_class mod);

#endif
