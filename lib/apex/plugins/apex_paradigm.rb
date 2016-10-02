module Apex
    module Plugins
        class ApexParadigm
            protected
            def initialize(config, port_map, aprsis)
                puts 'ApexParadigm inited'
            end
            
            public
            def run
                puts 'ApexParadigm ran'
            end
            
            public
            def stop
                puts 'ApexParadigm stop'
            end
            
            public
            def handle_packet(frame, recv_port, recv_port_name)
                puts 'ApexParadigm handled packet'
            end
        end

        PluginFactory.register_plugin(ApexParadigm)
    end
end