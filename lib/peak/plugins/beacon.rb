module Peak
    module Plugins
        class Beacon
            protected
            def initialize(config, port_map, aprsis)
                @port_configs = {}
                @aprsis = aprsis
                @running = false
                
                config.each do |section_name, section_content|
                    if section_name.start_with?('TNC ')
                        tnc_name = section_name.strip.split(' ')[1].strip
                        (1..section_content['port_count']).each do |port_id|
                            port_name = tnc_name + '-' + port_id.to_s
                            port = port_map[port_name]
                            port_section = 'PORT ' + port_name
                            @port_configs[port] = {:beacon_text => config[port_section]['beacon_text'],
                                                   :beacon_path => config[port_section]['beacon_path']
                            }
                        end
                    end
                end
            end
            
            private
            def self.now
                Time.now.to_i
            end
            
            public
            def run
                @running = true
        
                # Don't do anything in the first 30 seconds
                last_trigger = Beacon::now
                while @running and Beacon::now - last_trigger < 30
                    sleep(1)
                end
        
                # run every 600 second
                last_trigger = Beacon::now
                while @running
                    if Beacon::now - last_trigger >= 600
                        last_trigger = Beacon::now
                        @port_configs.each do |port, port_config|
                            frame = {:source => port.identifier,
                                     :destination => 'APRS',
                                     :path => port_config[:beacon_path],
                                     :text => port_config[:beacon_text]
                            }
                            port.write(frame)
                        end
                    else
                        sleep(1)
                    end
                end
            end
            
            public
            def stop
                @running = false
            end
            
            public
            def handle_packet(frame, recv_port)
            end
        end

        PluginFactory.register_plugin(Beacon)
    end
end