module Apex
    class TncPort
        protected
        def initialize(data_stream, name, identifier, net, port=0)
            @data_stream = data_stream
            @port = port
            @name = name
            @identifier = identifier
            @net = net
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
            return @data_stream.read(*args, **kwargs)
        end

        public
        def write(frame, *args, **kwargs)
            @data_stream.write(frame, @port, *args, **kwargs)
        end

        attr_reader :name, :net, :port, :identifier
    end
end