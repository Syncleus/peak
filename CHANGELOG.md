# Changelog

## 1.0.3

* Fixed a bug where crossband digipeating would send the packet out on the same TNC rather than the intended TNC.

## 1.0.2

* Added proper cleanup before exiting when a sigterm or sigint is received. This allows serial connections to be
  shutdown and KISS mode on the TNC to be exited.
* Added a Domain-specific Language for the routing and mangling of frames.
* By default frames are now preemptively digipeated.

## 1.0.1

* Added beacon plugin to transmit beacon every 10 minutes.
* Added id plugin to transmit id packet every 10 minutes.
* Added status plugin to transmit status packet every 10 minutes.
* Made plugin architecture multi-threaded.

## 1.0.0

* Initial release