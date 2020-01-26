#ifndef RSA_H_LEBBADI
#define RSA_H_LEBBADI

#include <gmpxx.h>
#include <vector>

std::vector<mpz_class> generateKey(int size = 4096, bool chinese = false);
mpz_class encrypt(mpz_class number, mpz_class exp, mpz_class mod);
mpz_class decrypt(mpz_class number, mpz_class exp, mpz_class mod);
mpz_class decrypt_chinese(mpz_class number, mpz_class p, mpz_class q, mpz_class dp, mpz_class dq, mpz_class qinv);

#endif
