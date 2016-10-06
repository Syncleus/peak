module Peak
    module Routing
        class Rules
            protected
            def initialize(frame, config, frame_port, next_target=nil)
                @frame = frame
                @next_target = next_target
                @config = config
                @frame_port = frame_port

                @port_info = {}
                config.each do |section_name, section_content|
                    if section_name.start_with?('TNC ')
                        tnc_name = section_name.strip.split(' ')[1].strip
                        if tnc_name != 'IGATE'
                            port_count = section_content['port_count']
            
                            (1..port_count).each do |port|
                                port_name = tnc_name + '-' + port.to_s
                                port_section_name = 'PORT ' + port_name
                                port_section = config[port_section_name]
                                port_identifier = port_section['identifier']
                                port_net = port_section['net']
                                tnc_port = port_section['tnc_port']
                
                                @port_info[port_name] = {
                                    :port_identifier => port_identifier,
                                    :port_net => port_net,
                                    :tnc_port => tnc_port
                                }
                            end
                        end
                    end
                end
            end

            private
            def self.args_parser(*args)
                if !args or !args.length or args.length <= 0
                    return nil
                end

                if !!args[0] == args[0] # if the first argument is a boolean
                    condition = args[0]
                    true_target = args.length >= 2 ? args[1] : :pass
                    false_target = args.length >= 3 ? args[2] : :pass
                else
                    condition = true
                    true_target = args.length >= 1 ? args[0] : :pass
                    false_target = args.length >= 2 ? args[1] : :pass
                end

                next_target = condition ? true_target : false_target

                {
                    :condition => condition,
                    :true_target => true_target,
                    :false_target => false_target,
                    :next_target => next_target
                }
            end

            private
            def do_next_target(next_target)
                if next_target != :pass
                    @next_target = next_target
                    throw :new_target
                end
                return
            end

            protected
            def filter(*args)
                args = Rules.args_parser(*args)
                Rules.do_next_target(args[:next_target])
            end

            protected
            def consume_next_hop(*args)
                args = Rules.args_parser(*args)

                catch(:done) do
                    @frame[:path].each do |hop|
                        unless hop.end_with? '*'
                            hop << '*'
                            throw :done
                        end
                    end
                end
                
                Rules.do_next_target(args[:next_target])
            end
            
            protected
            def seen?
                identifiers = @port_info.values.map { |info| info[:port_identifier] }
                if identifiers.include? @frame[:source]
                    return true
                end
                
                @frame[:path].each do |hop|
                    unless hop.end_with? '*'
                        return false
                    end
                    
                    if identifiers.include? hop.chomp('*')
                        return true
                    end
                end
                
                false
            end

            protected
            def destination_me?
                identifiers = @port_info.values.map { |info| info[:port_identifier] }
                if identifiers.include? @frame[:destination]
                    return true
                end
                false
            end

            public
            attr_reader :next_target, :frame
        end

        class Route
            @@chains = {}

            public
            def self.inbound_chain(&block)
                @@chains[:inbound] = {:target => :input, :block => block}
            end

            public
            def self.outbound_chain(&block)
                @@chains[:outbound] = {:target => :output, :block => block}
            end

            public
            def self.side_chain(name, target, &block)
                @@chains[name] = {:target => target, :block => block}
            end
        end

        # ==== This is the part the user will implement ======

        Route.inbound_chain {
            filter destination_me?, :pass, :forward
            filter :input # if this werent here packet would be dropped
        }

        Route.outbound_chain {
            filter :output # if this werent here packet would be dropped
        }

        Route.side_chain(:forward, :output) {
            filter seen?, :drop
            consume_next_hop
            filter :drop
        }

        # ==== Exiting custom code ========

        class Route
            public
            def self.handle_frame(frame, config, is_inbound, name)
                initial_chain = is_inbound ? :inbound : :outbound
                unless @@chains.key? initial_chain
                    return nil
                end
                
                rules = Rules.new(frame, config, name, initial_chain)
                more = true
                while more and rules.next_target != :input and rules.next_target != :output and rules.next_target != :drop
                    catch(:new_target) do
                        rules.instance_eval &@@chains[rules.next_target][:block]
                        more = false
                    end
                end

                if rules.next_target == :drop or !more
                    return nil
                end

                [{
                    :output_target => rules.next_target == :output ? name : nil,
                    :frame => rules.frame
                }]
            end
        end
    end
end