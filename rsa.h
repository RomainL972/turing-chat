#ifndef RSA_H_LEBBADI
#define RSA_H_LEBBADI

#include <gmpxx.h>
#include <vector>

std::vector<mpz_class> generateKey(int size);
mpz_class encrypt(mpz_class number, mpz_class exp, mpz_class mod);
mpz_class decrypt(mpz_class number, mpz_class exp, mpz_class mod);

#endif
