require 'yaml'
require 'peak/tnc_port'
require 'apex/aprs_kiss'
require 'kiss/constants'

module Peak
    def self.find_config(verbose, config_paths=[])
        config_file = 'peak.conf'
        rc_file = '.peakrc'
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
    
    def self.config_lookup_enforce(config_map, key)
        unless config_map.key?(key)
            echo_colorized_error('Invalid configuration, could not find an ' + key + ' attribute in section')
            return false
        end
        return true
    end
    
    def self.init_port_map(config)
        port_map = {}
        
        config.each do |section_name, section_content|
            if section_name.start_with?('TNC ')
                tnc_name = section_name.strip.split(' ')[1].strip
                if tnc_name == 'IGATE'
                    echo_colorized_error('IGATE was used as the name for a TNC in the configuration, this name is reserved')
                    return false
                end
            
                kiss_tnc = nil
                if config_lookup_enforce(section_content, 'com_port') and config_lookup_enforce(section_content, 'baud')
                    com_port = section_content['com_port']
                    baud = section_content['baud']
                    kiss_tnc = Apex::AprsKiss.new(Kiss::KissSerial.new(com_port, baud))
                else
                    return false
                end
                
                if section_content.key?('kiss_init')
                    kiss_init_string = section_content['kiss_init']
                    if kiss_init_string == 'MODE_INIT_W8DED'
                        kiss_tnc.connect(Kiss::MODE_INIT_W8DED)
                    elsif kiss_init_string == 'MODE_INIT_KENWOOD_D710'
                        kiss_tnc.connect(Kiss::MODE_INIT_KENWOOD_D710)
                    elsif kiss_init_string == 'NONE'
                        kiss_tnc.connect
                    else
                        echo_colorized_error('Invalid configuration, value assigned to kiss_init was not recognized: ' + kiss_init_string)
                        return false
                    end
                else
                    kiss_tnc.connect
                end
    
                unless config_lookup_enforce(section_content, 'port_count')
                    return false
                end
                
                port_count = section_content['port_count']
                
                (1..port_count).each do |port|
                    port_name = tnc_name + '-' + port.to_s
                    port_section_name = 'PORT ' + port_name
                    
                    unless config_lookup_enforce(config, port_section_name)
                        return false
                    end
                    port_section = config[port_section_name]
                    
                    unless config_lookup_enforce(port_section, 'identifier')
                        return false
                    end
                    port_identifier = port_section['identifier']

                    unless config_lookup_enforce(port_section, 'net')
                        return false
                    end
                    port_net = port_section['net']

                    unless config_lookup_enforce(port_section, 'tnc_port')
                        return false
                    end
                    tnc_port = port_section['tnc_port']
                    
                    port_map[port_name] = TncPort.new(kiss_tnc, port_name, port_identifier, port_net, true, tnc_port)
                end
            end
        end
        
        return port_map
    end
end