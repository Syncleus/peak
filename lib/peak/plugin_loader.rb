require 'peak/plugins/plugin_factory'

module Peak
    BUILTIN_PLUGINS = %w(peak/plugins/apex_paradigm peak/plugins/beacon peak/plugins/id peak/plugins/status)
    
    def self.all_plugins(extra_plugins=[])
        return BUILTIN_PLUGINS + extra_plugins
    end
    
    def self.load_plugins(plugins=BUILTIN_PLUGINS)
        plugins.each do |plugin|
            require plugin
        end
        return Plugins::PluginFactory.get_registered_plugins
    end
end