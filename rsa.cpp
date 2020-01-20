#include <gmp.h>
#include <gmpxx.h>
#include <random>
#include <iostream>

int main(int argc, char const *argv[]) {
    std::random_device dev;
    gmp_randclass r(gmp_randinit_mt);
    r.seed(dev());

    mpz_class p = r.get_z_bits(2048);
    mpz_class q;
    do {
         q = r.get_z_bits(2048);
    } while(p == q);

    mpz_class n = p * q;

    mpz_class m;
    mpz_class pm1 = p - 1;
    mpz_class qm1 = q - 1;
    mpz_lcm(m.get_mpz_t(), pm1.get_mpz_t(), qm1.get_mpz_t());

    mpz_class e = 65537;
    mpz_class d;

    mpz_invert(d.get_mpz_t(), e.get_mpz_t(), m.get_mpz_t());

    std::cout << "p: " << p.get_str(16) << std::endl
    << "q: " << q.get_str(16) << std::endl
    << "n: " << n.get_str(16) << std::endl
    << "e: " << e.get_str(16) << std::endl
    << "d: " << d.get_str(16) << std::endl;

    return 0;
}
