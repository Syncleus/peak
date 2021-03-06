module Peak
    module Routing
        class Rules
            protected
            def initialize(frame, config, frame_port, next_target=nil)
                @frame = frame
                @next_target = next_target
                @config = config
                @frame_port = frame_port
                @destination_port = frame_port

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

                                old_paradigm = port_section['old_paradigm']
                                unless old_paradigm
                                    old_paradigm = []
                                end

                                new_paradigm_all = port_section['new_paradigm']
                                new_paradigm = []
                                if new_paradigm_all and new_paradigm_all.length > 0
                                    new_paradigm_all.each do |new_paradigm_one|
                                        new_paradigm << {:target => new_paradigm_one['target'], :max_hops => new_paradigm_one['max_hops']}
                                    end
                                end

                                preemptive = port_section['preemptive']
                
                                @port_info[port_name] = {
                                    :port_identifier => port_identifier,
                                    :port_net => port_net,
                                    :tnc_port => tnc_port,
                                    :old_paradigm => old_paradigm,
                                    :new_paradigm => new_paradigm,
                                    :preemptive => preemptive
                                }
                            end
                        end
                    end
                end
            end

            private
            def self.args_parser(*args)
                if !args or !args.length or args.length <= 0
                    condition = args[0]
                    true_target = :pass
                    false_target = :pass
                elsif !!args[0] == args[0] # if the first argument is a boolean
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

            private
            def select_next_hop(hops)
                select_future_hops(hops)[0]
            end

            private
            def select_future_hops(hops)
                hops.select { |hop| !hop.end_with? '*'  }
            end

            private
            def select_net_band_hops(hops)
                hops.select { |hop| hop =~ /\d{1,4}M$/i  }
            end

            private
            def select_net_freq_hops(hops)
                hops.select { |hop| hop =~ /\d{1,4}M\d{1,3}$/i  }
            end

            private
            def select_net_hops(hops)
                hops.select { |hop| hop =~ /\d{1,4}M\d{0,3}$/i  }
            end

            private
            def net_freg_to_band_hops(hops)
                select_net_hops(hops).map { |hop| hop.gsub(/M\d{0,3}$/i, 'M')  }
            end

            private
            def all_my_names
                names = @port_info.values.map { |info| info[:port_identifier].upcase }
                names += net_freg_to_band_hops(@port_info.values.map {|info| info[:port_net].upcase })
                names += select_net_freq_hops(@port_info.values.map {|info| info[:port_net].upcase })
                names.uniq
            end

            private
            def self.array_upcase(things)
                things.map {|s|
                    if !s.is_a? Regexp
                        s.upcase
                    else
                        s
                    end
                }
            end

            private
            def self.is_hop_old_paradigm?(hop, old_paradigm)
                if old_paradigm.length <= 0
                    return false
                end

                old_paradigm = Rules.array_upcase(old_paradigm)
                hop = hop.upcase

                old_paradigm.each do |target|
                    if target.is_a? Regexp
                        if hop =~ target
                            return true
                        end
                    elsif hop == target
                        return true
                    end
                end

                false
            end

            private
            def self.is_hop_new_paradigm?(hop, new_paradigm_all)
                if new_paradigm_all.length <= 0
                    return false
                end

                hop = hop.upcase
                unless hop =~ /[A-Z]*-\d{1,2}/
                    return false
                end
                hop_split = hop.split('-')
                if !hop_split or hop_split.length != 2
                    return false
                end
                hop_target = hop_split[0]
                hop_hops = hop_split[1].to_i
                if hop_hops <= 0
                    return false
                end

                new_paradigm_all.each do |new_paradigm|
                    if new_paradigm[:target].is_a? Regexp
                        if hop_target =~ new_paradigm[:target]
                            return true
                        end
                    elsif hop_target == new_paradigm[:target].upcase
                        return true
                    end
                end

                false
            end

            private
            def self.is_hop_identifier_me(hop, identifiers)
                if identifiers.include? hop.upcase
                    true
                else
                    false
                end
            end

            private
            def self.consume_new_paradigm(hop)
                hop_split = hop.split('-')
                target = hop_split[0]
                hop_count = hop_split[1].to_i
                hop_count -= 1
                if hop_count > 0
                    hop.replace( target + '-' + hop_count.to_s )
                else
                    hop.replace(target + '*')
                end
            end

            protected
            def filter(*args)
                args = Rules.args_parser(*args)
                do_next_target(args[:next_target])
            end

            protected
            def route(*args, preemptive: nil)
                args = Rules.args_parser(*args)

                if has_next_hop? and args[:condition]
                    detected = false

                    port_name = @frame_port
                    port_info = @port_info[port_name]

                    if preemptive == nil
                        preemptive = port_info[:preemptive]
                        if preemptive == nil
                            preemptive = true
                        end
                    end

                    old_paradigm = nil
                    if port_info.key? :old_paradigm and port_info[:old_paradigm].length > 0
                        old_paradigm = Rules.array_upcase(port_info[:old_paradigm])
                    end


                    new_paradigm = nil
                    if port_info.key? :new_paradigm and port_info[:new_paradigm].length > 0
                        new_paradigm = port_info[:new_paradigm]
                    end


                    target = nil
                    next_hop = select_next_hop(@frame[:path])
                    if all_my_names.include? next_hop.upcase or Rules.is_hop_old_paradigm?(next_hop, old_paradigm)
                        target = next_hop.dup
                        next_hop << '*'
                    elsif Rules.is_hop_new_paradigm?(next_hop, new_paradigm)
                        target = next_hop.dup
                        Rules.consume_new_paradigm(next_hop)
                    end

                    if preemptive
                        future_hops = select_future_hops(@frame[:path])
                        identifiers = @port_info.values.map { |info| info[:port_identifier].upcase }
                        future_hops.reverse.each do |hop|
                            if detected
                                hop << '*'
                            elsif identifiers.include? hop.upcase
                                target = hop.dup
                                hop << '*'
                                detected = true
                            end
                        end
                    end

                    if target
                        @port_info.each do |name, info|
                            identifier = info[:port_identifier].upcase
                            net_freq = info[:port_net]
                            net_band = net_freq.dup.gsub(/M\d{0,3}$/i, 'M')

                            if target == identifier or target == net_freq or target == net_band
                                @destination_port = @frame_port
                            end
                        end
                    end
                end

                do_next_target(args[:next_target])
            end
            
            protected
            def seen?
                identifiers = @port_info.values.map { |info| info[:port_identifier].upcase }
                if identifiers.include? @frame[:source].upcase
                    return true
                end
                
                @frame[:path].each do |hop|
                    unless hop.end_with? '*'
                        return false
                    end
                    
                    if identifiers.include? hop.upcase.chomp('*')
                        return true
                    end
                end
                
                false
            end

            protected
            def destination_me?
                identifiers = @port_info.values.map { |info| info[:port_identifier].upcase }
                if identifiers.include? @frame[:destination].upcase
                    true
                else
                    false
                end
            end

            protected
            def has_next_hop?
                @frame[:path].each do |hop|
                    unless hop.end_with? '*'
                        return true
                    end
                end
                return false
            end

            protected
            def next_hop_identifier_me?
                unless has_next_hop?
                    return false
                end

                identifiers = @port_info.values.map { |info| info[:port_identifier].upcase }
                Rules.is_hop_identifier_me(select_next_hop(@frame[:path]), identifiers)
            end

            protected
            def future_hop_identifier_me?
                unless has_next_hop?
                    return false
                end

                identifiers = @port_info.values.map { |info| info[:port_identifier].upcase }
                if (identifiers & select_future_hops(Rules.array_upcase(@frame[:path]))).empty?
                    false
                else
                    true
                end
            end

            protected
            def next_hop_net_band_me?
                unless has_next_hop?
                    return false
                end

                net_bands = net_freg_to_band_hops(@port_info.values.map {|info| info[:port_net].upcase })
                next_bands = select_net_band_hops([select_next_hop(@frame[:path]).upcase])

                if next_bands.length <= 0 or net_bands.length <= 0
                    return false
                end

                next_band = next_bands[0]

                if net_bands.include? next_band
                    false
                else
                    true
                end
            end

            protected
            def future_hop_net_band_me?
                unless has_next_hop?
                    return false
                end

                net_bands = net_freg_to_band_hops(@port_info.values.map {|info| info[:port_net].upcase })
                next_bands = Rules.array_upcase(select_net_band_hops(@frame[:path]))

                if next_bands.length <= 0 or net_bands.length <= 0
                    return false
                end

                if (net_bands & next_bands).empty?
                    true
                else
                    false
                end
            end

            protected
            def next_hop_net_freq_me?
                unless has_next_hop?
                    return false
                end

                net_freqs = select_net_freq_hops(@port_info.values.map {|info| info[:port_net].upcase })
                next_freqs= select_net_freq_hops([select_next_hop(@frame[:path]).upcase])

                if next_freqs.length <= 0 or net_freqs.length <= 0
                    return false
                end

                next_band = next_bands[0]

                if net_bands.include? next_band
                    false
                else
                    true
                end
            end

            protected
            def future_hop_net_freq_me?
                unless has_next_hop?
                    return false
                end

                net_freqs = select_net_freq_hops(@port_info.values.map {|info| info[:port_net].upcase })
                next_freqs = select_net_freq_hops(select_future_hops(Rules.array_upcase(@frame[:path])))

                if next_freqs.length <= 0 or net_freqs.length <= 0
                    return false
                end

                if (net_freqs & next_freqs).empty?
                    true
                else
                    false
                end
            end

            protected
            def next_hop_old_paradigm?
                unless has_next_hop?
                    return false
                end

                port_name = @frame_port
                port_info = @port_info[port_name]

                if !port_info.key? :old_paradigm or port_info[:old_paradigm].length <= 0
                    return false
                end

                old_paradigm = Rules.array_upcase(port_info[:old_paradigm])
                next_hop = select_next_hop(@frame[:path]).upcase

                Rules.is_hop_old_paradigm?(next_hop, old_paradigm)
            end

            protected
            def future_hop_old_paradigm?
                unless has_next_hop?
                    return false
                end

                port_name = @frame_port
                port_info = @port_info[port_name]

                if !port_info.key? :old_paradigm or port_info[:old_paradigm].length <= 0
                    return false
                end

                old_paradigm = Rules.array_upcase(port_info[:old_paradigm])
                future_hops = select_future_hops(@frame[:path]).map { |s| s.upcase }

                old_paradigm.each do |target|
                    if target.is_a? Regexp
                        future_hops.each do |hop|
                            if hop =~ target
                                return true
                            end
                        end
                    elsif future_hops.include? target
                        return true
                    end
                end

                false
            end

            protected
            def next_hop_new_paradigm?
                unless has_next_hop?
                    return false
                end

                port_name = @frame_port
                port_info = @port_info[port_name]

                if !port_info.key? :new_paradigm or port_info[:new_paradigm].length <= 0
                    return false
                end

                new_paradigm_all = port_info[:new_paradigm]
                next_hop = select_next_hop(@frame[:path]).upcase

                Rules.is_hop_new_paradigm?(next_hop, new_paradigm_all)
            end

            protected
            def future_hop_new_paradigm?
                unless has_next_hop?
                    return false
                end

                port_name = @frame_port
                port_info = @port_info[port_name]

                if !port_info.key? :new_paradigm or port_info[:new_paradigm].length <= 0
                    return false
                end

                new_paradigm_all = port_info[:new_paradigm]
                future_hops = select_future_hops(@frame[:path]).map { |s| s.upcase }
                

                new_paradigm_all.each do |new_paradigm|
                    if new_paradigm[:target].is_a? Regexp
                        future_hops.each do |hop|
                            if hop.include? '-'
                                hop_split = hop.split('-')
                                if hop_split and hop_split.length == 2
                                    hop_target = hop_split[0]
                                    hop_hops = hop_split[1].to_i
                                    if hop_hops > 0 and hop_target =~ new_paradigm[:target]
                                        return true
                                    end
                                end
                            end
                        end
                    elsif future_hops.include? new_paradigm[:target].upcase
                        return true
                    end
                end

                false
            end

            protected
            def next_hop_net_me?
                if next_hop_net_band_me? or next_hop_net_freq_me?
                    true
                else
                    false
                end
            end

            protected
            def future_hop_net_me?
                if future_hop_net_band_me? or future_hop_net_freq_me?
                    true
                else
                    false
                end
            end

            protected
            def next_hop_paradigm?
                if next_hop_new_paradigm? or next_hop_old_paradigm?
                    true
                else
                    false
                end
            end

            protected
            def future_hop_paradigm?
                if future_hop_new_paradigm? or future_hop_old_paradigm?
                    true
                else
                    false
                end
            end

            protected
            def next_hop_me?
                if next_hop_net_me? or next_hop_identifier_me? or next_hop_paradigm?
                    true
                else
                    false
                end
            end

            protected
            def future_hop_me?
                if future_hop_net_me? or future_hop_identifier_me? or future_hop_paradigm?
                    true
                else
                    false
                end
            end

            protected
            def mine?
                if future_hop_me? or destination_me?
                    true
                else
                    false
                end
            end

            public
            attr_reader :next_target, :frame, :destination_port
        end

        class Route
            @@chains = {}

            public
            def self.inbound_chain(&block)
                @@chains[:inbound] = block
            end

            public
            def self.outbound_chain(&block)
                @@chains[:outbound] = block
            end

            public
            def self.side_chain(name, &block)
                @@chains[name] = block
            end

            public
            def self.reset
                @@chains.clear
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

        Route.side_chain(:forward) {
            filter seen?, :drop
            route future_hop_me?, :output, :drop
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
                        rules.instance_eval &@@chains[rules.next_target]
                        more = false
                    end
                end

                if rules.next_target == :drop or !more
                    return nil
                end

                {
                    :output_target => rules.next_target == :output ? rules.destination_port : nil,
                    :frame => rules.frame
                }
            end
        end
    end
end