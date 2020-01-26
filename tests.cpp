#include "rsa.h"
#include <iostream>
#include <vector>
#include <gmp.h>
#include <gmpxx.h>
#include <string>
#include <chrono>

using namespace std::chrono;

int main(int argc, char const *argv[]) {

    auto genStart = high_resolution_clock::now();
    std::vector<mpz_class> key = generateKey(4096, true);
    auto genStop = high_resolution_clock::now();

    std::vector<std::string> names = {"n", "e", "d", "p", "q", "dp", "dq", "qinv"};

    for (size_t i = 0; i < key.size(); i++) {
        std::cout << names[i] << " : " << key[i].get_str(16) << std::endl;
    }

    mpz_class encrypt_test("6549679876413510300000146987984561654987653165498798");

    std::cout << "Clair: " << encrypt_test.get_str() << std::endl;

    auto cryptStart = high_resolution_clock::now();
    mpz_class cypher = encrypt(encrypt_test, key[1], key[0]);
    auto cryptStop = high_resolution_clock::now();

    std::cout << "Cypher: " << cypher.get_str(16) << std::endl;

    auto decryptStart = high_resolution_clock::now();
    mpz_class clear = decrypt(cypher, key[2], key[0]);
    auto decryptStop = high_resolution_clock::now();

    std::cout << "Nouveau clair: " << clear.get_str() << std::endl;

    auto durationGen = duration_cast<microseconds>(genStop - genStart);
    auto durationCrypt = duration_cast<microseconds>(cryptStop - cryptStart);
    auto durationDecrypt = duration_cast<microseconds>(decryptStop - decryptStart);

    std::cout << "gen : " << durationGen.count() << std::endl;
    std::cout << "crypt : " << durationCrypt.count() << std::endl;
    std::cout << "decrypt : " << durationDecrypt.count() << std::endl;

    return 0;
}
