
Changelog
=========

0.0.5
-----


0.0.4
-----

* Colorized the output from the plugins.
* Removed packet_cache argument from plugins, it is no longer needed.
* Mechanisms added to ensure plugins can not send the same packet twice, plugins no longer need to handle this explicitly.
* Fixed a bug where packets can be digipeated multiple times.

0.0.3
-----

* Reordered changelog version entries.
* Fixed several mistakes in the README.

0.0.2
-----

* The configfile command line argument added.
* When no configfile argument present APEX will now search multiple default paths to find a configuration file.
* Changed LICENSE file text to include the full text of the Apache Software License version 2.
* Colorized some of the output.
* Changed the way plugins are discovered, they can now be installed anywhere.
* Fixed a bug in the APRS-IS class which threw a broken pipe error.
* Refactored several classes and renamed them: Kiss class now has two subclasses and AprsInternetServer is renamed to IGate
* Encapsulated IGate connection with a buffer that automatically reconnects when disconnected.
* Removed a few obsolete and unused util functions.
* Fix several errors thrown due to missing sections in the configuration file.

0.0.1
-----

* First release on PyPI.
