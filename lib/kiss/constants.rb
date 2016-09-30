module KISS
    # KISS Special Characters
    # http://en.wikipedia.org/wiki/KISS_(TNC)#Special_Characters
    FEND = 0xC0
    FESC = 0xDB
    TFEND = 0xDC
    TFESC = 0xDD

    # "FEND is sent as FESC, TFEND"
    FESC_TFEND = [KISS::FESC] + [KISS::TFEND]

    # "FESC is sent as FESC, TFESC"
    FESC_TFESC = [KISS::FESC] + [KISS::TFESC]

    # KISS Command Codes
    # http://en.wikipedia.org/wiki/KISS_(TNC)#Command_Codes
    DATA_FRAME = 0x00
    TX_DELAY = 0x01
    PERSISTENCE = 0x02
    SLOT_TIME = 0x03
    TX_TAIL = 0x04
    FULL_DUPLEX = 0x05
    SET_HARDWARE = 0x06
    RETURN = 0xFF

    DEFAULT_KISS_CONFIG_VALUES = {
        'TX_DELAY': 40,
        'PERSISTENCE': 63,
        'SLOT_TIME': 20,
        'TX_TAIL': 30,
        'FULL_DUPLEX': 0,
    }

    # This command will exit KISS mode
    MODE_END = [192, 255, 192, 13]

    # This will start kiss on a WA8DED or LINK>.<NORD firmware
    MODE_INIT_W8DED = [13, 27, 64, 75, 13]
    MODE_INIT_LINKNORD = KISS::MODE_INIT_W8DED

    # Kenwood D710
    MODE_INIT_KENWOOD_D710 = [72, 66, 32, 49, 50, 48, 48, 13, # HB 1200
                              75, 73, 83, 83, 32, 79, 78, 13, # KISS ON
                              82, 69, 83, 84, 65, 82, 84, 13] # RESTART

    # Kantronics TNCs
    MODE_INIT_KANTRONICS = [13, # Blank
                            73, 78, 84, 32, 75, 73, 83, 83, 13, # INT KISS
                            82, 69, 83, 84, 65, 82, 84, 13] # RESTART

    # TINY2 TNC (TNC2)
    MODE_INIT_TINY2 = [13, # Blank
                       75, 73, 83, 83, 32, 79, 78, 13, # KISS ON
                       82, 69, 83, 84, 65, 82, 84, 13] # RESTART

    # Advanced Electronic Application (later Timewave) PK-232 TNC
    MODE_INIT_PK232 = [42, 126, 13, # *~
                       69, 88, 80, 69, 82, 84, 32, 79, 78, 13, # EXPERT ON
                       75, 73, 83, 83, 32, 79, 78, 13, # KISS ON
                       82, 69, 83, 84, 65, 82, 84, 13] # RESTART
end