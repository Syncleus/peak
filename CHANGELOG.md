# Changelog

## 1.0.2

* Added proper cleanup before exiting when a sigterm or sigint is received. This allows serial connections to be
  shutdown and KISS mode on the TNC to be exited.

## 1.0.1

* Added beacon plugin to transmit beacon every 10 minutes.
* Added id plugin to transmit id packet every 10 minutes.
* Added status plugin to transmit status packet every 10 minutes.
* Made plugin architecture multi-threaded.

## 1.0.0

* Initial release