#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <vector>
#include <gmp.h>
#include <gmpxx.h>
#include "rsa.h"

#define KEYSIZE 4096

static PyObject *
rsa_generateKey(PyObject *self, PyObject *args)
{
    std::vector<mpz_class> key = generateKey(KEYSIZE);

    PyObject* tuple;
    tuple = Py_BuildValue(
        "(NNN)",
        PyUnicode_FromString(key[0].get_str(16).c_str()),
        PyUnicode_FromString(key[1].get_str(16).c_str()),
        PyUnicode_FromString(key[2].get_str(16).c_str())
    );

    return tuple;
}

static PyObject*
rsa_encrypt(PyObject *self, PyObject *args) {
    char *textStr, *expStr, *modStr;
    if (!PyArg_ParseTuple(args, "ssy", &expStr, &modStr, &textStr))
        return NULL;

    mpz_class exp, mod, text;
    text.set_str(textStr, 16);
    exp.set_str(expStr, 16);
    mod.set_str(modStr, 16);

    mpz_class cypher = encrypt(text, exp, mod);

    return PyBytes_FromString(cypher.get_str(16).c_str());
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
      "Decrypt an encrypted string."},
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
