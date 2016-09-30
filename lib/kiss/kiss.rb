require 'thread'
require 'abstraction'
require_relative 'constants'

module KISS
    class KISS
        abstract

        protected
        def initialize(strip_df_start=true, exit_kiss=true)
            @strip_df_start = strip_df_start
            @exit_kiss = exit_kiss
            @lock = Mutex.new
        end

        private
        def self.strip_df_start(frame)
            while frame[0] == KISS::DATA_FRAME
                frame.shift
            end
            frame.strip
            return frame
        end

        private
        def self.escape_special_codes(raw_code_bytes)
            encoded_bytes = []
            raw_code_bytes.each do |raw_code_byte|
                if raw_code_byte == KISS::FESC
                    encoded_bytes += KISS::FESC_TFESC
                elsif raw_code_byte == KISS::FEND
                    encoded_bytes += KISS::FESC_TFEND
                else
                    encoded_bytes += [raw_code_byte]
                end
                return encoded_bytes
            end
        end

        private
        def self.command_byte_combine(port, command_code)
            if port > 127 or port < 0
                raise 'port out of range'
            elsif command_code > 127 or command_code < 0
                raise 'command_Code out of range'
            end
            return (port << 4) & command_code
        end

        protected
        def write_setting(name, value)
            # return self.write_interface(
            #         KISS::FEND +
            #         getattr(kiss_constants, name.upper()) +
            #         Kiss.__escape_special_codes(value) +
            #         kiss_constants.FEND
            # )
        end

        def connect(mode_init=None, *args, **kwargs)
        end

        def close()
            if @exit_kiss
                self.write_interface(KISS::MODE_END)
            end
        end

        def read()
            @lock.synchronize do
                # read stuff
            end
        end

        def write(frame_bytes, port=0)
            @lock.synchronize do
                # write stuff
            end
        end
    end
end