require 'colorize'
require 'yaml'
require 'kiss/kiss_serial'
require 'aprs/aprs_kiss'
require 'apex/app_info'
require 'apex/plugins/plugin_factory'

module Apex
    # BUILTIN_PLUGINS = %w(apex/plugins/apexparadigm apex/plugins/beacon apex/plugins/id apex/plugins/status)
    BUILTIN_PLUGINS = %w(apex/plugins/beacon)

    def self.all_plugins(extra_plugins=[])
        return BUILTIN_PLUGINS + extra_plugins
    end

    def self.load_plugins(plugins=BUILTIN_PLUGINS)
        plugins.each do |plugin|
            require plugin
        end
        return Plugins::PluginFactory.get_registered_plugins
    end

    def self.find_config(verbose, config_paths=[])
        config_file = 'apex.conf'
        rc_file = '.apexrc'
        cur_path = config_file
        home_path = File.join(Dir.home, rc_file)
        etc_path = File.join('', 'etc', config_file)
        config_paths = [cur_path, home_path, etc_path] + config_paths

        if verbose
            puts 'Searching for configuration file in the following locations: ' + config_paths.inspect
        end

        config_paths.each do |config_path|
            if File.file?(config_path)
                return YAML::load_file(config_path)
            end
        end

        return nil
    end

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

    def self.main
        config = find_config(true)
        p config
        
        activated_plugins = []
        plugins = load_plugins
        plugins.each do |plugin|
            activated_plugin = plugin.new(nil, nil, nil)
            activated_plugins << activated_plugin
            activated_plugin.run
        end

        kiss = Kiss::KissSerial.new('/dev/ttyUSB1', 9600)
        aprs_kiss = Aprs::AprsKiss.new(kiss)
        aprs_kiss.connect(Kiss::MODE_INIT_KENWOOD_D710)

        # Transmit a beacon when we first start
        beacon_frame = {:source => 'WI2ARD-2',
                        :destination => 'APRS',
                        :path => ['WIDE1-1', 'WIDE2-2'],
                        :text => '!/:=i@;N.G& --PHG5790/G/D R-I-R H24 C30'}
        aprs_kiss.write(beacon_frame)
        echo_color_frame(beacon_frame, 'TNC', false)

        # Display any packets we read in.
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
