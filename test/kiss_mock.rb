require_relative '../lib/kiss/kiss_abstract'

module Kiss
    class KissMock < KissAbstract

        def initialize(strip_df_start=true)
            super(strip_df_start)
            @read_from_interface = []
            @sent_to_interface = []
        end

        protected
        def read_interface
            if @read_from_interface.length == 0
                return nil
            end
            return @read_from_interface.shift
        end

        protected
        def write_interface(data)
            @sent_to_interface << data
        end

        public
        def clear_interface
            @read_from_interface = []
            @sent_to_interface = []
        end

        public
        def add_read_from_interface(raw_frame)
            @read_from_interface << raw_frame
        end

        public
        def get_sent_to_interface
            return @sent_to_interface
        end
    end
end