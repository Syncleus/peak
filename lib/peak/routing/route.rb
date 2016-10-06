module Peak
    module Routing
        class Rules
            protected
            def initialize(frame, chains, next_target)
                @frame = frame
                @chains = chains
                @next_target = next_target
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

            attr_reader :next_target, :frame
        end

        class Routing
            @chains = {}

            public
            def inbound_chain(&block)
                @chains[:inbound] = {:target => :input, :block => block}
            end

            public
            def outbound_chain(&block)
                @chains[:outbound] = {:target => :output, :block => block}
            end

            public
            def side_chain(name, target, &block)
                @chains[name] = {:target => target, :block => block}
            end
        end

        route = Routing.new

        # ==== This is the part the user will implement ======

        route.inbound_chain {
            filter destination_me?, :pass, :forward
            filter :input # not needed, showing input chain always terminates in recv
        }

        route.outbound_chain {
            filter :output #not needed, showing send target is the end of the output target
        }

        route.side_chain(:forward, :output) {
            filter seen?, :drop, :pass
            consume_next_hop
            filter :foo
        }

        # ==== Exiting custom code ========

        class Routing
            public
            def handle_frame(frame,is_inbound=true)
                rules = Rules.new(frame, @chains, is_inbound ? :inbound : :outbound)
                while rules.next_target != :input and rules.next_target != :output and rules.next_target != :drop
                    catch(:new_target) do
                        rules.instance_eval &chains[rules.next_target][:block]
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