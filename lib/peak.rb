require 'peak/echo'
require 'peak/config_loader'
require 'peak/plugin_loader'

module Peak

    def self.main
        config = find_config(true)
        port_map = init_port_map(config)
        
        active_plugins = {}
        plugins = load_plugins
        plugins.each do |plugin|
            active_plugin = plugin.new(config, port_map, nil)
            active_plugin_thread = Thread.new {
                active_plugin.run
            }
            active_plugins[active_plugin] =active_plugin_thread
        end

        # Transmit a beacon when we first start
        beacon_frame = {:source => 'WI2ARD-2',
                        :destination => 'APRS',
                        :path => ['WIDE1-1', 'WIDE2-2'],
                        :text => '!/:=i@;N.G& --PHG5790/G/D R-I-R H24 C30'}
        port_map.values.each do |tnc_port|
            tnc_port.write(beacon_frame)
        end

        # Display any packets we read in.
        while true
            port_map.values.each do |tnc_port|
                frame = tnc_port.read
                if frame
                    active_plugins.each_key do |plugin|
                        plugin.handle_packet(frame, tnc_port)
                    end
                else
                    sleep(1)
                end
            end
        end
    end
end
