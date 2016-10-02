module Apex
    module Plugins
        class Status
            protected
            def initialize(config, port_map, aprsis)
                puts 'Status inited'
            end
            
            public
            def run
                puts 'Status ran'
            end
            
            public
            def stop
                puts 'Status stop'
            end
            
            public
            def handle_packet(frame, recv_port, recv_port_name)
                puts 'Status handled packet'
            end
        end

        PluginFactory.register_plugin(Status)
    end
end