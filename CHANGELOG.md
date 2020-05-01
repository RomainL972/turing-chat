# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2020-05-01
### Added
- Username functionnality

### Changed
- Instead of importing everything, go back to `from tkinter import *`
- The callback to print messages is now by default in logging mode

### Fixed
- Make msg_list readonly in gui
- The program won't crash when an unknown message is received anymore

## [1.1.1] - 2020-04-02
### Added
- sendQuit callback in API, called when "/quit" entered

### Fixed
- add threading in GUI so it doesn't hang and prints messages

## [1.1.0] - 2020-03-12
### Added
- Indication when message comes from other person in the GUI

### Changed
- API now always has a client and a server, not always connected, no change in functions
- Client can be restarted
- Server doesn't automatically listen for connections
- Change minimum resolution in GUI

### Fixed
- Connexion makes itself inaccessible in API before closing
- Better formatting in gui.py
- Replace Turinchat by TuringChat
- Fixed test.decrypt in test_rsa

## [1.0.0] - 2020-03-03
### Added
- Argument for /connect in the API
- First Release Version

## [0.14.0] - 2020-03-02
### Added
- Unit tests for backend.py file using pytest
- Switch to decide if backend should get private key on init
- A Graphical User Interface

### Fixed
- Delete connexion in API when client or server closed
- Handle exception when adding port mapping or getting external ip in upnp

## [0.13.1] - 2020-03-01
### Added
- example code using the API (sample.py)
- this CHANGELOG.md

### Fixed
- Update README to reflect changes in program
- Make UPnP module conditional so it works on Windows
- Removed all print() calls outside cli.py
- Handle server already listening on server start

## [0.13.0] - 2020-02-18
### Added
- api.py, interface between cli/gui and everything else

### Changed
- Moved most code of cli.py to api.py in Interface class

### Removed
- noPrint arg in printMessage function

## [0.12.0] - 2020-02-18
### Added
- Re-add saving private key to file
- Re-add message parsing for commands
- Proper quit with "/quit"
- Commands for starting client or server

### Changed
- Log most messages with rdyReadFunc or rdyRead

### Fixed
- Handle refused connexion from server
- Removed useless number from ConnexionThread
- Remove upnp at the end if added at the beginning

### Removed
- test_input.py, which was a test for message formatting in cli

## [0.11.0] - 2020-02-17
### Added
- cli.py file
- SocketClient class in client.py
- Callbacks for when ready to send or when receiving messages
- ConnexionThread class used by server or client when connexion is established

### Changed
- Moved python files to src/ folder

### Fixed
- Server and client can now both send and receive messages
- UPnP only deletes port mapping if it already exists
- Re-add private key striping

### Removed
- Useless getPublicKey function

## [0.10.0] - 2020-02-14
### Added
- README.md and LICENSE (MIT)

### Changed
- Replace backend functions with RSAKey and TuringChat classes

### Fixed
- server send pubkey to client, client to server messaging works

### Removed
- message parsing for commands temporarily

## [0.9.1] - 2020-02-13
### Fixed
- Use the received public key
- Delete UPnP mapping before readding it
- Strip private key when sending it
- Removed useless import
- Install dependencies in GitHub Action

## [0.9.0] - 2020-02-13
### Added
- keyFromJson and keyToJson functions
- keyFromBase64 and keyToBase64 functions
- getPublicIp function
- settings.py
- basic messaging API
- client can send messages to server (if same key)
- GitHub Action

### Changed
- Moved message parsing to backend

### Fixed
- Solved flake8 warnings

### Removed
- Text padding functions
- rsaBackend.py
- Basic server (not threaded)

## [0.8.0] - 2020-02-06
### Added
- Text padding functions

### Changed
- Updated gitignore

## [0.7.1] - 2020-02-04
### Added
- requirements.txt file

### Fixed
- Handle UPnP failure

## [0.7.0] - 2020-01-29
### Added
- Python library using gmpy2 to use rsa
- Threaded server from internet
- backend.py close to rsaBackend.py but using python library

### Removed
- C++ Extension

## [0.6.0] - 2020-01-26
### Changed
- Moved c++ files to subdirectory
- Use CMake to build extension
- Use rsaBackend to encrypt/decrypt

## [0.5.0] - 2020-01-25
### Added
- rsaBackend file
- Chinese decryption option
- C++ test file
- private key saved in file

### Changed
- Improved test.py

## [0.4.0] - 2020-01-23
### Changed
- Go back to default decryption algorithm
- Integrate rsa c++ extension in Python

### Removed
- Javascript code

## [0.3.0] - 2020-01-20
### Added
- Replace C extension with C++
- Javascript openpgp code
- Chinese algorithm decryption

### Removed
- Build files and executables

## [0.2.0] - 2019-09-12
### Added
- C Extension library for RSA

## [0.1.0] - 2019-09-05
### Added
- Basic server and client
- Use regex to parse commands

[2.0.0]: https://github.com/RomainL972/isn/compare/v1.1.1...v2.0.0
[1.1.1]: https://github.com/RomainL972/isn/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/RomainL972/isn/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/RomainL972/isn/compare/v0.14.0...v1.0.0
[0.14.0]: https://github.com/RomainL972/isn/compare/v0.13.1...v0.14.0
[0.13.1]: https://github.com/RomainL972/isn/compare/v0.13.0...v0.13.1
[0.13.0]: https://github.com/RomainL972/isn/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/RomainL972/isn/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/RomainL972/isn/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/RomainL972/isn/compare/v0.9.1...v0.10.0
[0.9.1]: https://github.com/RomainL972/isn/compare/v0.9.0...v0.9.1
[0.9.0]: https://github.com/RomainL972/isn/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/RomainL972/isn/compare/v0.7.1...v0.8.0
[0.7.1]: https://github.com/RomainL972/isn/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/RomainL972/isn/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/RomainL972/isn/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/RomainL972/isn/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/RomainL972/isn/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/RomainL972/isn/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/RomainL972/isn/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/RomainL972/isn/releases/tag/v0.1.0
