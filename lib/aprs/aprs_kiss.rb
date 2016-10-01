require_relative '../kiss/constants'

module APRS
    class APRSKiss

        protected
        def initialize(data_stream)
            @data_stream = data_stream
            @lock = Mutex.new
        end

        private
        def self.decode_frame(raw_frame)
            frame = {}
            frame_len = raw_frame.length

            if frame_len > 16
                (0...frame_len - 2).each do |raw_slice|
                    # Is address field length correct?
                    if raw_frame[raw_slice] & 0x01 and ((raw_slice + 1) % 7) == 0
                        i = (raw_slice.to_f + 1.0) / 7.0
                        # Less than 2 callsigns?
                        if 1.0 < i < 11.0
                            if raw_frame[raw_slice + 1] & 0x03 == 0x03 and [0xf0, 0xcf].include? raw_frame[raw_slice + 2]
                                text_as_array = raw_frame[raw_slice + 3..-1].map { |b| chr(b) }
                                frame['text'] = text_as_array.join
                                frame['destination'] = identity_as_string(extract_callsign(raw_frame))
                                frame['source'] = identity_as_string(__extract_callsign(raw_frame[7..-1]))
                                frame['path'] = extract_path(i.to_i, raw_frame)
                                return frame
                            end
                        end
                    end
                end
            end
            frame
        end

        private
        def self.extract_path(start, raw_frame)
            full_path = []

            (2...start).each do |i|
                path = identity_as_string(extract_callsign(raw_frame[i * 7..-1]))
                if path
                    if raw_frame[i * 7 + 6] & 0x80
                        full_path << [path, '*'].join
                    else
                        full_path << path
                    end
                end
            end
            full_path
        end

        private
        def self.extract_callsign(raw_frame)
            callsign_as_array = raw_frame[0...6].map { |x| chr(x >> 1) }
            callsign = callsign_as_array.join.strip
            ssid = (raw_frame[6] >> 1) & 0x0f
            return {'callsign': callsign, 'ssid': ssid}
        end

        private
        def self.identity_as_string(identity)
            if identity['ssid'] > 0
                return [identity['callsign'], identity['ssid'].to_s].join('-')
            else
                return identity['callsign']
            end
        end

        private
        def self.encode_frame(frame)
            enc_frame = encode_callsign(parse_identity_string(frame['destination'])) + encode_callsign(parse_identity_string(frame['source']))
            frame['path'].each do |p|
                enc_frame += encode_callsign(parse_identity_string(p))
            end

            return enc_frame[0..-1] + [enc_frame[-1] | 0x01] + [KISS::SLOT_TIME] + [0xf0] + frame['text'].map { |c| ord(c) }
        end

        private
        def self.encode_callsign(callsign)
            call_sign = callsign['callsign']

            enc_ssid = (callsign['ssid'] << 1) | 0x60

            if call_sign.include? '*'
                call_sign.gsub!(/\*/,'')
                enc_ssid |= 0x80
            end

            while call_sign.length < 6
                call_sign = [call_sign, ' '].join
            end

            return call_sign.map { |p| ord(p) << 1 } + [enc_ssid]
        end

        private
        def self.parse_identity_string(identity_string)
            # If we are parsing a spent token then first lets get rid of the astresick suffix.
            if identity_string[-1] == '*'
                identity_string = identity_string[0..-1]
            end

            if identity_string.include? '-'
                call_sign, ssid = identity_string.split('-')
            else
                call_sign = identity_string
                ssid = 0
            end

            return {'callsign': call_sign, 'ssid': int(ssid)}
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
        def write(frame, *args, **kwargs)
            @lock.synchronize do
                encoded_frame = encode_frame(frame)
                @data_stream.write(encoded_frame, *args, **kwargs)
            end
        end

        public
        def read(*args, **kwargs)
            @lock.synchronize do
                frame = @data_stream.read(*args, **kwargs)
                if frame&.length
                    return decode_frame(frame)
                else
                    return nil
                end
            end
        end
    end
end