module Peak
    module Plugins
        class Id
            protected
            def initialize(config, port_map, aprsis)
                puts 'Id inited'
            end
            
            public
            def run
                puts 'Id ran'
            end
            
            public
            def stop
                puts 'Id stop'
            end
            
            public
            def handle_packet(frame, recv_port, recv_port_name)
                puts 'Id handled packet'
            end
        end

        PluginFactory.register_plugin(Id)
    end
end