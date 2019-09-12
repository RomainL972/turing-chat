#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <gmp.h> //On inclut la bibliothèque gmp
#include <sodium.h>
#include <stdio.h>

#define KEYSIZE 16

static PyObject *
rsa_generateKey(PyObject *self, PyObject *args)
{
    int randomInt = randombytes_uniform(10);
    char minChar[KEYSIZE + 1], maxChar[KEYSIZE + 2];
    char output[KEYSIZE * 2];
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

    //Init GMP vars
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

    PyObject* tuple;
    tuple = Py_BuildValue(
        "(NNN)",
        PyBytes_FromString(mpz_get_str(NULL, 16, n)),
        PyBytes_FromString(mpz_get_str(NULL, 16, c)),
        PyBytes_FromString(mpz_get_str(NULL, 16, u))
    );

    return tuple;
}

static PyObject*
rsa_encrypt(PyObject *self, PyObject *args) {
    PyObject *expStr, *modStr;
    char* text;
    if (!PyArg_ParseTuple(args, "SSs", &expStr, &modStr, &text))
        return NULL;

    mpz_t exp, mod, letter;
    mpz_init_set_str(exp, PyBytes_AsString(expStr), 16);
    mpz_init_set_str(mod, PyBytes_AsString(modStr), 16);
    mpz_init(letter);

    PyObject* list = PyList_New(0);
    Py_INCREF(list);

    for (int i = 0; text[i] != '\0'; i++) {
        mpz_set_ui(letter, text[i]);
        mpz_powm(letter, letter, exp, mod);
        PyList_Append(list, PyBytes_FromString(mpz_get_str(NULL, 16, letter)));
    }

    return list;
}

static PyObject*
rsa_decrypt(PyObject *self, PyObject *args) {
    PyObject *list;
    PyObject *expStr, *modStr;
    Py_ssize_t size;

    if (!PyArg_ParseTuple(args, "SSO", &expStr, &modStr, &list))
        return NULL;

    size = PyList_Size(list);
    mpz_t exp, mod, letter;
    mpz_init_set_str(exp, PyBytes_AsString(expStr), 16);
    mpz_init_set_str(mod, PyBytes_AsString(modStr), 16);
    mpz_init(letter);
    for(Py_ssize_t i = 0; i < size; i++) {
        mpz_set_str(letter, PyBytes_AsString(PyList_GetItem(list, i)), 16);
        mpz_powm(letter, letter, exp, mod);
        unsigned int out = mpz_get_ui(letter);
        printf("%c", out);
    }

    return Py_None;
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
