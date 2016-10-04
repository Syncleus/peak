module Peak
    module Plugins
        class ApexParadigm
            protected
            def initialize(config, port_map, aprsis)
            end
            
            public
            def run
            end
            
            public
            def stop
            end
            
            public
            def handle_packet(frame, recv_port)
            end
        end

        PluginFactory.register_plugin(ApexParadigm)
    end
end