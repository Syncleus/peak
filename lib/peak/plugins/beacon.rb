module Peak
    module Plugins
        class Beacon
            protected
            def initialize(config, port_map, aprsis)
                puts 'beacon inited'
            end
            
            public
            def run
                puts 'beacon ran'
            end
            
            public
            def stop
                puts 'beacon stop'
            end
            
            public
            def handle_packet(frame, recv_port)
                puts 'Beacon handled packet'
            end
        end

        PluginFactory.register_plugin(Beacon)
    end
end