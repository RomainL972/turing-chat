#include <gmp.h> //On inclut la bibliothèque gmp
#include <sodium.h>
#include <stdio.h>
#include <string.h>

#define KEYSIZE 2048

int main(int argc, char const *argv[]) {
    int randomInt = randombytes_uniform(10);
    char minChar[KEYSIZE + 1], maxChar[KEYSIZE + 2];
    char output[KEYSIZE + 1];
    /**
      * KEYSIZE+1 is for 4096-bit number + \0
      * KEYSIZE+2 is for 4097-bit number + \0
      */

    //Create min and max
    memset (minChar, '0', KEYSIZE);
    memset (maxChar, '0', KEYSIZE + 1);
    minChar[0] = '1';
    maxChar[0] = '1';
    minChar[KEYSIZE] = '\0';
    maxChar[KEYSIZE + 1] = '\0';


    mpz_t p, q, min, max, interval, n, qminus1, c, gcd, m, u, v;
    mpz_init(p);
    mpz_init(q);
    mpz_init(n);
    mpz_init(interval);
    mpz_init(qminus1);
    mpz_init(gcd);
    mpz_init(m);
    mpz_init(u);
    mpz_init(v);
    mpz_init_set_ui(c, 65536);
    mpz_init_set_str(min, minChar, 2);
    mpz_init_set_str(max, maxChar, 2);

    //Set interval to max-min+1
    mpz_sub(interval, max, min);
    mpz_add_ui(interval, interval, 1);

    //Init random number generator
    gmp_randstate_t state;
    gmp_randinit_mt(state);
    gmp_randseed_ui(state, randomInt);

    //Generate random 4096-bit prime
    mpz_urandomm(p, state, interval);
    mpz_add(p, p, min);
    mpz_nextprime(p, p);

    //Do it again
    randomInt = randombytes_uniform(10);
    gmp_randseed_ui(state, randomInt);
    mpz_urandomm(q, state, interval);
    mpz_add(q, q, min);
    mpz_nextprime(q, q);

    mpz_mul(n, p, q);

    mpz_sub_ui(m, p, 1);
    mpz_sub_ui(qminus1, q, 1);
    mpz_lcm(m, m, qminus1);

    do {
        mpz_add_ui(c, c, 1);
        mpz_gcdext(gcd, u, v, c, m);
    } while(mpz_cmp_ui(gcd, 1));

    //If u < 2
    if(mpz_cmp_ui(u, 2) < 0) {
        mpz_t k;
        mpz_init_set_ui(k, 2);
        mpz_sub(k, k, u);
        mpz_neg(m, m);
        mpz_fdiv_q(k, k, m);
        mpz_neg(m, m);
        mpz_mul(k, k, m);
        mpz_sub(u, u, k);
    }
    if(mpz_cmp(u, m) > 0) {
        mpz_t k;
        mpz_init(k);
        mpz_sub(k, m, u);
        mpz_neg(m, m);
        mpz_fdiv_q(k, k, m);
        mpz_neg(m, m);
        mpz_mul(k, k, m);
        mpz_sub(u, u, k);
    }

    gmp_printf("M: %Zd\n", m);
    gmp_printf("N: %Zd, C: %Zd\n", n, c);
    gmp_printf("U: %Zd\n", u);

    mpz_t encryptedLetter, letter;
    mpz_init(encryptedLetter);
    mpz_init_set_ui(letter, 'c');

    gmp_printf("Clear: %Zd\n", letter);
    mpz_powm (encryptedLetter, letter, c, n );
    gmp_printf("Encrypted: %Zd\n", encryptedLetter);
    mpz_powm(letter, encryptedLetter, u, n);
    gmp_printf("Decrypted: %Zd\n", letter);

    //return PyBytes_FromString(output);
    return 0;
}
