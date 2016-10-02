require 'kiss/kiss_serial'
require 'aprs/aprs_kiss'
require 'apex/app_info'
require 'apex/plugins/plugin_factory'
require 'apex/echo'
require 'apex/config_loader'
require 'apex/plugin_loader'

module Apex

    def self.main
        config = find_config(true)
        puts 'config:'
        p config
        puts
        
        puts 'port_map:'
        port_map = init_port_map(config)
        p port_map
        puts
        
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
