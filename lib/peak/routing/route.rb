module Peak
    module Routing
        class Rules
            protected
            def initialize(frame, config, next_target=nil)
                @frame = frame
                @next_target = next_target
                @config = config

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
                
                                @port_info[port_identifier] = {
                                    :port_name => port_name,
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
                if !args&.length or args.length <= 0
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
            def self.do_next_target(next_target)
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
            def seen?
                if @port_info.key? @frame[:source]
                    return true
                end
                
                @frame[:path].each do |hop|
                    unless hop.end_with? '*'
                        return false
                    end
                    
                    if @port_info.key? hop.chomp('*')
                        return true
                    end
                end
                
                false
            end
            

            attr_reader :next_target, :frame
        end

        class Routing
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

        Routing.inbound_chain {
            filter destination_me?, :pass, :forward
            filter :input # not needed, showing input chain always terminates in recv
        }

        Routing.outbound_chain {
            filter :output #not needed, showing send target is the end of the output target
        }

        Routing.side_chain(:forward, :output) {
            filter seen?, :drop, :pass
            consume_next_hop
            filter :foo
        }

        # ==== Exiting custom code ========

        class Routing
            public
            def self.handle_frame(frame, config, is_inbound=true)
                rules = Rules.new(frame, config, is_inbound ? :inbound : :outbound)
                while rules.next_target != :input and rules.next_target != :output and rules.next_target != :drop
                    catch(:new_target) do
                        rules.instance_eval &@@chains[rules.next_target][:block]
                    end
                end

                if rules.next_target == :drop
                    return nil
                end

                {
                    :target => rules.next_target,
                    :frame => rules.frame
                }
            end
        end
    end
end