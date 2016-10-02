require 'yaml'

module Apex
    def self.find_config(verbose, config_paths=[])
        config_file = 'apex.conf'
        rc_file = '.apexrc'
        cur_path = config_file
        home_path = File.join(Dir.home, rc_file)
        etc_path = File.join('', 'etc', config_file)
        config_paths = [cur_path, home_path, etc_path] + config_paths
        
        if verbose
            puts 'Searching for configuration file in the following locations: ' + config_paths.inspect
        end
        
        config_paths.each do |config_path|
            if File.file?(config_path)
                return YAML::load_file(config_path)
            end
        end
        
        return nil
    end
end