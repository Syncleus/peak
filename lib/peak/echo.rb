require 'colorize'

module Peak
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
            puts (port_name + ' >> ').colorize(:color => :magenta, :mode => :bold) + formatted_aprs
        end
    end
    
    def self.echo_colorized_error(text)
        puts 'Error: '.colorize(:color => :red, :mode => [:bold, :blink]) + text.colorize(:bold)
    end
    
    def self.echo_colorized_warning(text)
        puts 'Warning: '.colorize(:color => :yellow) + text
    end
end
