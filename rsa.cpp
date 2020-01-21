#include <gmp.h>
#include <gmpxx.h>
#include <random>
#include <iostream>
#include <vector>
#include <string>
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

    mpz_class dp, dq, qinv;
    dp = d % mpz_class(p-1);
    dq = d % mpz_class(q-1);
    mpz_invert(qinv.get_mpz_t(), q.get_mpz_t(), p.get_mpz_t());


    std::vector<mpz_class> array = {n, e, d, p, q, m, dp, dq, qinv};
    return array;
}

mpz_class encrypt(mpz_class number, mpz_class exp, mpz_class mod) {
    mpz_powm(number.get_mpz_t(), number.get_mpz_t(), exp.get_mpz_t(), mod.get_mpz_t());
    return number;
}

mpz_class decrypt(mpz_class number, mpz_class p, mpz_class q, mpz_class dp, mpz_class dq, mpz_class qinv) {
    mpz_class m1, m2, h, m;
    mpz_powm(m1.get_mpz_t(), number.get_mpz_t(), dp.get_mpz_t(), p.get_mpz_t());
    mpz_powm(m2.get_mpz_t(), number.get_mpz_t(), dq.get_mpz_t(), q.get_mpz_t());
    h = (qinv * (m1-m2)) % p;
    m = (m2 + h * q) % (p * q);
    return m;
}

int main(int argc, char const *argv[]) {
    std::vector<mpz_class> key;
    key = generateKeys(4096);
    char letter;

    std::string parts[] = {"n", "e", "d", "p", "q", "m", "dp", "dq", "qinv"};
    for (size_t i = 0; i < 9; i++) {
        std::cout << parts[i] << ": " << key[i].get_str() << std::endl;
    }

    std::cout << "Lettre : ";
    std::cin >> letter;

    mpz_class clear = letter;
    mpz_class cypher, newclear;
    cypher = encrypt(clear, key[1], key[0]);
    newclear = decrypt(cypher, key[3], key[4], key[6], key[7], key[8]);

    std::cout << "Clear : " << clear.get_str(10) << std::endl;
    std::cout << "Cypher : " << cypher.get_str(10) << std::endl;
    std::cout << "New clear : " << (char)newclear.get_ui() << std::endl;

    return 0;
}
