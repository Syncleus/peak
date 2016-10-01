require 'test/unit'
require_relative 'kiss_mock'

module Kiss
    # KG6WTF>S7TSUV,MTOSO-2,WIDE2*,qAR,KF6FIR-10:`17El#X-/kg6wtf@gosselinfamily.com
    ENCODED_FRAME = [192, 0, 75, 71, 54, 87, 84, 70, 62, 83, 55, 84, 83, 85, 86, 44, 77, 84, 79, 83, 79, 45, 50, 44, 87, 73,
                     68, 69, 50, 42, 44, 113, 65, 82, 44, 75, 70, 54, 70, 73, 82, 45, 49, 48, 58, 96, 49, 55, 69, 108, 35,
                     88, 45, 47, 107, 103, 54, 119, 116, 102, 64, 103, 111, 115, 115, 101, 108, 105, 110, 102, 97, 109, 105,
                     108, 121, 46, 99, 111, 109, 192]
    DECODED_FRAME = [75, 71, 54, 87, 84, 70, 62, 83, 55, 84, 83, 85, 86, 44, 77, 84, 79, 83, 79, 45, 50, 44, 87, 73, 68,
                     69, 50, 42, 44, 113, 65, 82, 44, 75, 70, 54, 70, 73, 82, 45, 49, 48, 58, 96, 49, 55, 69, 108, 35,
                     88, 45, 47, 107, 103, 54, 119, 116, 102, 64, 103, 111, 115, 115, 101, 108, 105, 110, 102, 97, 109,
                     105, 108, 121, 46, 99, 111, 109]
    
    class TestKiss < Test::Unit::TestCase
        def test_read
            kiss_mock = KissMock.new
            kiss_mock.add_read_from_interface(ENCODED_FRAME)
            translated_frame = kiss_mock.read
            assert_equal DECODED_FRAME, translated_frame
        end

        def test_write
            kiss_mock = KissMock.new
            kiss_mock.write(DECODED_FRAME)
            all_raw_frames = kiss_mock.get_sent_to_interface
            assert_equal ENCODED_FRAME, all_raw_frames[0]
        end

        def test_new_abstract_kiss
            assert_raise(AbstractClassError) { KissAbstract.new }
        end
    end
end