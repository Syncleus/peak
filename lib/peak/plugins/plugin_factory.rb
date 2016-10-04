module Peak
    module Plugins
        class PluginFactory
            @@plugins = []
            
            def self.register_plugin(new_plugin)
                if new_plugin
                    @@plugins << new_plugin
                    @@plugins.uniq!
                end
            end
            
            def self.get_registered_plugins
                return @@plugins.dup
            end
        end
    end
end