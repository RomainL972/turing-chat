#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <gmp.h> //On inclut la bibliothèque gmp
#include <gmpxx.h>
#include <random>
#include <iostream>
#include <string>

#define KEYSIZE 2048

static PyObject *
rsa_generateKey(PyObject *self, PyObject *args)
{
    //Generate p and q primes
    mpz_class p, q;
    std::random_device rd;
    gmp_randclass rand(gmp_randinit_mt);
    rand.seed(rd());
    p = rand.get_z_bits(KEYSIZE);
    mpz_nextprime(p.get_mpz_t(), p.get_mpz_t());
    do {
        q = rand.get_z_bits(KEYSIZE);
        mpz_nextprime(q.get_mpz_t(), q.get_mpz_t());
    } while(p == q);

    //Calculate n and m
    mpz_class n(p * q);

    mpz_class m(p - 1), qminus1(q - 1);
    mpz_lcm(m.get_mpz_t(), m.get_mpz_t(), qminus1.get_mpz_t());

    //Set e
    mpz_class e(65537);

    //Calculate everything else
    mpz_class gcd, u, v;
    mpz_gcdext(gcd.get_mpz_t(), u.get_mpz_t(), v.get_mpz_t(), e.get_mpz_t(), m.get_mpz_t());

    //If u < 2
    if(u < 2) {
        mpz_class k(2);
        k -= u;
        m = -m;
        mpz_fdiv_q(k.get_mpz_t(), k.get_mpz_t(), m.get_mpz_t());
        m = -m;
        k *= m;
        u -= k;
    }
    if(u > m) {
        mpz_class k;
        k = m - u;
        m = -m;
        mpz_fdiv_q(k.get_mpz_t(), k.get_mpz_t(), m.get_mpz_t());
        m = -m;
        k *= m;
        u -= k;
    }

    PyObject* tuple;
    tuple = Py_BuildValue(
        "(NNN)",
        PyBytes_FromString(mpz_get_str(NULL, 16, n.get_mpz_t())),
        PyBytes_FromString(mpz_get_str(NULL, 16, e.get_mpz_t())),
        PyBytes_FromString(mpz_get_str(NULL, 16, u.get_mpz_t()))
    );

    return tuple;
}

static PyObject*
rsa_encrypt(PyObject *self, PyObject *args) {
    char *textStr, *expStr, *modStr;
    if (!PyArg_ParseTuple(args, "sss", &expStr, &modStr, &textStr))
        return NULL;

    mpz_class exp, mod, text;
    text.set_str(textStr, 16);
    exp.set_str(expStr, 16);
    mod.set_str(modStr, 16);

    mpz_powm(text.get_mpz_t(), text.get_mpz_t(), exp.get_mpz_t(), mod.get_mpz_t());

    return PyBytes_FromString(text.get_str(16).c_str());
}

static PyObject*
rsa_decrypt(PyObject *self, PyObject *args) {
    return rsa_encrypt(self, args);
}

static PyMethodDef RSAMethods[] = {
    {"generateKey",  rsa_generateKey, METH_VARARGS,
     "Generate a 4096-bit RSA key."},
    {"encrypt", rsa_encrypt, METH_VARARGS,
     "Encrypt a string."},
     {"decrypt", rsa_decrypt, METH_VARARGS,
      "Decrypt an encrypted list."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef rsamodule = {
    PyModuleDef_HEAD_INIT,
    "rsa",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    RSAMethods
};

PyMODINIT_FUNC
PyInit_rsa(void)
{
    return PyModule_Create(&rsamodule);
}
