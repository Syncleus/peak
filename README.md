# APEX

APEX is a next generation APRS based protocol. This repository represents the reference implementation and is a full features application for digipeating across multiple AX.25 KISS TNC devices using the full APEX stack.

For more information on the project please check out [the project's home page](http://apexprotocol.com/).

## Running the app

Right now the setup.py has a few bugs in it. So you can either try to fix it, wait for us to fix it, or simply install
the prerequsites manually. The following is a list of the preequsites that need to be installed.

    pynmea2 >= 1.4.2
    pyserial >= 2.7
    requests >= 2.7.0
    cachetools >= 1.1.5

The application is written for python 3 specifically, it may not work with python 2. Once installed copy the
apex.cfg.example file over to apex.cfg in the same directory, then edit the file and replace it with your details. Next
just run the application with the following command.

    python ./comterminal.py

There isnt much to the application right now, so thats all you should need to run it. Digipeating will occur
automatically and respond to the WIDEN-n paradigm as well as your own callsign. Cross-band repeating is enabled right
now but only by specifying the call sign directly. The application is still pre-release so more features and
configuration options should be added soon.
