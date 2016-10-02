require 'apex/plugins/plugin_factory'

module Apex
    BUILTIN_PLUGINS = %w(apex/plugins/apex_paradigm apex/plugins/beacon apex/plugins/id apex/plugins/status)
    
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