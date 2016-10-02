require 'colorize'
require 'kiss/kiss_serial'
require 'aprs/aprs_kiss'
require 'apex/app_info'

module Apex
    def self.echo_color_frame(frame, port_name, direction_in)
        formatted_aprs = [frame[:source].colorize(:green), frame[:destination].colorize(:blue)].join('>')
        paths = []
        frame[:path].each do |path|
            paths << path.colorize(:cyan)
        end
        paths = paths.join(',')
        if frame[:path] and frame[:path].length > 0
            formatted_aprs = [formatted_aprs, paths].join(',')
        end
        formatted_aprs += ':'
        formatted_aprs += frame[:text]
        if direction_in
            puts (port_name + ' << ').colorize(:magenta) + formatted_aprs
        else
            # TODO : make this bold and/or blink
            puts (port_name + ' >> ').colorize(:magenta).bold.blink + formatted_aprs
        end
    end

    def self.main
        kiss = Kiss::KissSerial.new('/dev/ttyUSB1', 9600)
        aprs_kiss = Aprs::AprsKiss.new(kiss)
        aprs_kiss.connect(Kiss::MODE_INIT_KENWOOD_D710)

        while true
            frame = aprs_kiss.read
            if frame
                echo_color_frame(frame, 'TNC',  true)
            else
                sleep(1)
            end
        end
    end
end
