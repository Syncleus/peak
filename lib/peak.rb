require 'kiss/kiss_serial'
require 'apex/aprs_kiss'
require 'peak/app_info'
require 'peak/plugins/plugin_factory'
require 'peak/echo'
require 'peak/config_loader'
require 'peak/plugin_loader'

module Peak

    def self.main
        config = find_config(true)
        port_map = init_port_map(config)
        
        activated_plugins = []
        plugins = load_plugins
        plugins.each do |plugin|
            activated_plugin = plugin.new(nil, nil, nil)
            activated_plugins << activated_plugin
            activated_plugin.run
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
                unless frame
                    sleep(1)
                end
            end
        end
    end
end