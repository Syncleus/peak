require 'peak/echo'
require 'peak/config_loader'
require 'peak/plugin_loader'
require 'peak/routing/route'

module Peak

    def self.main
        config = find_config(true)
        unless config
            echo_colorized_error('Could not find a valid configuration file in any of the default locations')
            return
        end

        port_map = init_port_map(config)
        unless port_map
            echo_colorized_error('Configuration could not be loaded,  format was invalid.')
            return
        end

        Signal.trap('INT') { throw :sig }
        Signal.trap('TERM') { throw :sig }
        
        active_plugins = {}
        plugins = load_plugins
        plugins.each do |plugin|
            active_plugin = plugin.new(config, port_map, nil)
            active_plugin_thread = Thread.new {
                active_plugin.run
            }
            active_plugins[active_plugin] = active_plugin_thread
        end

        # Handle any packets we read in.
        catch (:sig) do
            while true
                something_read = false
                port_map.values.each do |tnc_port|
                    frame = tnc_port.read
                    if frame
                        something_read = true
                        routed_frame = Routing::Route.handle_frame(frame, config, true, tnc_port.name)
                        if routed_frame
                            if routed_frame[:output_target]
                                port_map[routed_frame[:output_target]].write(routed_frame[:frame])
                            else
                                active_plugins.each_key do |plugin|
                                    plugin.handle_packet(routed_frame[:frame], tnc_port)
                                end
                            end
                        end
                    end
                end
                unless something_read
                    sleep(1)
                end
            end
        end

        puts
        puts 'Shutdown signal caught, shutting down...'

        # Let's cleanup some stuff before exiting.
        active_plugins.keys.each do |plugin|
            plugin.stop
        end
        active_plugins.values.each do |plugin_thread|
            plugin_thread.join
        end
        port_map.values.each do |port|
            port.close
        end
        
        puts 'Peak successfully shutdown.'
    end
end
