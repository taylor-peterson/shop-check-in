ID_STRING_NONE = "gibberish gibberish gibberish"
ID_STRING_ONE = ";40155181\x00"
ID_STRING_ONE_WITHOUT_START_END_CHARACTERS = "40155181"
ID_STRING_ONE_IN_THE_MIDDLE = "gibberish ;40155181\x00 gibberish"
ID_STRING_ONE_BROKEN_UP = ";40155 gibberish 181\x00"
ID_STRING_TWO_BACK_TO_BACK = ";40155181\x00;40155181\x00"
ID_STRING_TWO_SEPARATED = ";40155181\x00 gibberish ;40155181\x00"

# TODO: figure out how to spoof receiving keyboard input.
    # Can't actually send the appropriate keypresses as \x00 isn't supported.
    # Plus, doing so wouldn't be proper as it could have unwanted side-effects.


class TestIdLogger(object):

    def test_id_logger_none(self):
        assert False

    def test_id_logger_one(self):
        assert False

    def test_id_logger_one_without_start_end_characters(self):
        assert False

    def test_id_logger_one_in_middle(self):
        assert False

    def test_id_logger_one_id_broken_up(self):
        assert False

    def test_id_logger_two_ids_back_to_back(self):
        assert False

    def test_id_logger_two_ids_separated(self):
        assert False