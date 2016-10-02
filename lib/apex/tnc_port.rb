require 'apex/echo'

module Apex
    class TncPort
        protected
        def initialize(data_stream, name, identifier, net, echo_frames=false, port=0)
            @data_stream = data_stream
            @port = port
            @name = name
            @identifier = identifier
            @net = net
            @ech_frames = echo_frames
        end

        public
        def connect(*args, **kwargs)
            @data_stream.connect(*args, **kwargs)
        end

        public
        def close(*args, **kwargs)
            @data_stream.close(*args, **kwargs)
        end

        public
        def read(*args, **kwargs)
            read_frame = @data_stream.read(*args, **kwargs)
            if @echo_frames
                Apex::echo_color_frame(read_frame, @name, true)
            end
            return read_frame
        end

        public
        def write(frame, *args, **kwargs)
            @data_stream.write(frame, @port, *args, **kwargs)
            if @echo_frames
                Apex::echo_color_frame(frame, @name, false)
            end
        end

        attr_reader :name, :net, :port, :identifier
    end
end