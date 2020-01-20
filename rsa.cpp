#include <gmp.h>
#include <gmpxx.h>
#include <random>
#include <iostream>
#include <vector>
#include "rsa.h"

std::vector<mpz_class> generateKeys(int size) {
    std::random_device dev;
    gmp_randclass r(gmp_randinit_mt);
    r.seed(dev());

    mpz_class p = r.get_z_bits(size/2);
    mpz_nextprime(p.get_mpz_t(), p.get_mpz_t());
    mpz_class q;
    do {
         q = r.get_z_bits(size/2);
         mpz_nextprime(q.get_mpz_t(), q.get_mpz_t());
    } while(p == q);

    mpz_class n = p * q;

    mpz_class m = lcm(mpz_class(p-1), mpz_class(q-1));

    mpz_class e = 65537;
    mpz_class d;

    mpz_invert(d.get_mpz_t(), e.get_mpz_t(), m.get_mpz_t());

    std::vector<mpz_class> array = {n, e, d};
    return array;
}

mpz_class crypt(mpz_class number, mpz_class exp, mpz_class mod) {
    mpz_powm(number.get_mpz_t(), number.get_mpz_t(), exp.get_mpz_t(), mod.get_mpz_t());
    return number;
}

int main(int argc, char const *argv[]) {
    std::vector<mpz_class> key;
    key = generateKeys(4096);
    char letter;

    std::cout << "n: " << key[0].get_str(10) << std::endl
    << "e: " << key[1].get_str(10) << std::endl
    << "d: " << key[2].get_str(10) << std::endl;

    std::cout << "Lettre : ";
    std::cin >> letter;

    mpz_class clear = letter;
    mpz_class cypher, newclear;
    cypher = crypt(clear, key[1], key[0]);
    newclear = crypt(cypher, key[2], key[0]);

    std::cout << "Clear : " << clear.get_str(10) << std::endl;
    std::cout << "Cypher : " << cypher.get_str(10) << std::endl;
    std::cout << "New clear : " << (char)newclear.get_ui() << std::endl;

    return 0;
}
