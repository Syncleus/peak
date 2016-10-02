require 'colorize'
require 'kiss/kiss_serial'
require 'aprs/aprs_kiss'
require 'apex/app_info'

module Apex
    def self.echo_color_frame(frame, direction_in)
        formatted_aprs = [frame[:source].colorize(:green), frame[:destination].colorize(:blue)].join('>')
        paths = []
        frame[:path].each do |path|
            paths << path.colorize(:cyan)
        end
        paths = ','.join(paths)
        if frame['path']
            formatted_aprs = ','.join([formatted_aprs, paths])
        end
        formatted_aprs += ':'
        formatted_aprs += frame['text']
        if direction_in
            click.echo(click.style(port_name + ' << ', fg='magenta') + formatted_aprs)
        else
            click.echo(click.style(port_name + ' >> ', fg='magenta', bold=True, blink=True) + formatted_aprs)
        end
    end

    def self.main
        kiss = Kiss::KissSerial.new('/dev/ttyUSB1', 9600)
        aprs_kiss = Aprs::AprsKiss.new(kiss)
        aprs_kiss.connect(Kiss::MODE_INIT_KENWOOD_D710)

        while true
            frame = aprs_kiss.read
            if frame
                echo_color_frame(frame)
            else
                sleep(1)
            end
        end
    end
end
