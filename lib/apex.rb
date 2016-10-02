require 'kiss/kiss_serial'
require 'aprs/aprs_kiss'

module Apex
    VERSION = "0.0.1"

    def self.main
        kiss = Kiss::KissSerial.new('/dev/ttyUSB1', 9600)
        aprs_kiss = Aprs::AprsKiss.new(kiss)
        aprs_kiss.connect(Kiss::MODE_INIT_KENWOOD_D710)

        while true
            frame = aprs_kiss.read
            if frame
                p frame
            else
                sleep(1)
            end
        end
    end
end
