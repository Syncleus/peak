require 'thread'
require 'abstraction'
require 'kiss/constants'

module Kiss
    class KissAbstract
        abstract

        protected
        def initialize(strip_df_start=true)
            @strip_df_start = strip_df_start
            @frame_buffer = []
            @lock = Mutex.new
        end

        private
        def self.strip_df_start(frame)
            while frame[0] == DATA_FRAME
                frame.shift
            end
            while frame[0] and frame[0].chr == ' '
                frame.shift
            end
            while frame[-1] and frame[-1].chr == ' '
                frame.pop
            end
            frame
        end

        private
        def self.escape_special_codes(raw_code_bytes)
            encoded_bytes = []
            raw_code_bytes.each do |raw_code_byte|
                if raw_code_byte == FESC
                    encoded_bytes += FESC_TFESC
                elsif raw_code_byte == FEND
                    encoded_bytes += FESC_TFEND
                else
                    encoded_bytes += [raw_code_byte]
                end
            end
            encoded_bytes
        end

        private
        def self.command_byte_combine(port, command_code)
            if port > 127 or port < 0
                raise 'port out of range'
            elsif command_code > 127 or command_code < 0
                raise 'command_Code out of range'
            end
            (port << 4) & command_code
        end

        protected
        def write_setting(command, value)
            write_interface([FEND] + [command] + escape_special_codes(value) + [FEND])
        end

        private
        def fill_buffer
            new_frames = []
            read_buffer = []
            read_data = read_interface
            while read_data and read_data.length > 0
                split_data = [[]]
                read_data.each do |read_byte|
                    if read_byte == FEND
                        split_data << []
                    else
                        split_data[-1] << read_byte
                    end
                end
                len_fend = split_data.length

                # No FEND in frame
                if len_fend == 1
                    read_buffer += split_data[0]
                    # Single FEND in frame
                elsif len_fend == 2
                    # Closing FEND found
                    if split_data[0]
                        # Partial frame continued, otherwise drop
                        new_frames << read_buffer + split_data[0]
                        read_buffer = []
                        # Opening FEND found
                    else
                        new_frames << read_buffer
                        read_buffer = split_data[1]
                    end
                    # At least one complete frame received
                elsif len_fend >= 3
                    (0...len_fend - 1).each do |i|
                        read_buffer_tmp = read_buffer + split_data[i]
                        if read_buffer_tmp.length > 0
                            new_frames << read_buffer_tmp
                            read_buffer = []
                        end
                    end
                    if split_data[len_fend - 1]
                        read_buffer = split_data[len_fend - 1]
                    end
                end
                # Get anymore data that is waiting
                read_data = read_interface
            end

            new_frames.each do |new_frame|
                if new_frame.length > 0 and new_frame[0] == 0
                    if @strip_df_start
                        new_frame = KissAbstract.strip_df_start(new_frame)
                    end
                    @frame_buffer << new_frame
                end
            end
        end

        public
        def connect(mode_init=nil, *args, **kwargs)
        end

        public
        def close
        end

        public
        def read(*args, **kwargs)
            @lock.synchronize do
                if @frame_buffer.length == 0
                    fill_buffer
                end

                if @frame_buffer.length > 0
                    return_frame = @frame_buffer[0]
                    @frame_buffer.shift
                    return return_frame
                else
                    return nil
                end
            end
        end

        public
        def write(frame_bytes, port=0, *args, **kwargs)
            @lock.synchronize do
                kiss_packet = [FEND] + [KissAbstract.command_byte_combine(port, DATA_FRAME)] +
                    KissAbstract.escape_special_codes(frame_bytes) + [FEND]

                write_interface(kiss_packet)
            end
        end
    end
end