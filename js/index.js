var openpgp = require('openpgp'); // use as CommonJS, AMD, ES6 module or via window.openpgp
var options, encrypted;

var options = {
    userIds: [{ name:'Jon Smith', email:'jon@example.com' }], // multiple user IDs
    rsaBits: 4096,                                            // RSA key size
    passphrase: 'super long and hard to guess secret'         // protects the private key
};

openpgp.generateKey(options).then(function(key) {
    var privkey = key.privateKeyArmored; // '-----BEGIN PGP PRIVATE KEY BLOCK ... '
    var pubkey = key.publicKeyArmored;   // '-----BEGIN PGP PUBLIC KEY BLOCK ... '
    var revocationCertificate = key.revocationCertificate; // '-----BEGIN PGP PUBLIC KEY BLOCK ... '
    console.log(privkey)
    console.log(pubkey)
});
