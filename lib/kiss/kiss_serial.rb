require 'serialport'
require_relative 'kiss_abstract'

module Kiss
    class KissSerial < KissAbstract

        DEFAULT_READ_BYTES = 1000
        SERIAL_READ_TIMEOUT = -1

        protected
        def initialize(com_port,
                       baud=38400,
                       parity=SerialPort::NONE,
                       stop_bits=1,
                       byte_size=8,
                       read_bytes=DEFAULT_READ_BYTES,
                       strip_df_start=true)
            super(strip_df_start)

            @com_port = com_port
            @baud = baud
            @parity = parity
            @stop_bits = stop_bits
            @byte_size = byte_size
            @read_bytes = read_bytes
            @serial = nil
            @exit_kiss = false
        end

        protected
        def read_interface
            read_data = @serial.read(@read_bytes)
            p read_data
            if read_data
                return read_data.chars.map { |c| c.ord }
            else
                return nil
            end
        end

        protected
        def write_interface(data)
            @serial.write(data)
        end

        public
        def connect(mode_init=nil, **kwargs)
            super

            @serial = SerialPort.new(@com_port, @baud, @byte_size, @stop_bits, @parity)
            @serial.read_timeout = SERIAL_READ_TIMEOUT

            if mode_init
                @serial.write(mode_init)
                @exit_kiss = true
            else
                @exit_kiss = false
            end

            # Previous verious defaulted to Xastir-friendly configs. Unfortunately
            # those don't work with Bluetooth TNCs, so we're reverting to None.
            if kwargs
                kwargs.each do |name,value|
                    write_setting(name, value)
                end
            end
        end

        public
        def close
            super

            if @exit_kiss
                write_interface(MODE_END)
            end

            if @serial == nil or @serial.closed?
                raise 'Attempting to close before the class has been started.'
            else
                @serial.close
            end
        end
    end
end