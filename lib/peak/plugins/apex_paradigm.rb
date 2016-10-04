module Peak
    module Plugins
        class PeakParadigm
            protected
            def initialize(config, port_map, aprsis)
                puts 'PeakParadigm inited'
            end
            
            public
            def run
                puts 'PeakParadigm ran'
            end
            
            public
            def stop
                puts 'PeakParadigm stop'
            end
            
            public
            def handle_packet(frame, recv_port)
                puts 'PeakParadigm handled packet'
            end
        end

        PluginFactory.register_plugin(PeakParadigm)
    end
end