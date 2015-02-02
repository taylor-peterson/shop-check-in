import timeout
import time

class TestTimeout:

    def test_timeout(self):
        @timeout.timeout
        def infinity():
            while True:
                pass
        assert not infinity()

    def test_timeout_func_completes(self):
        @timeout.timeout
        def f():
            return 'done'
        assert f() == 'done'

    def test_make_timeout_time(self):
        @timeout.make_timeout(1)
        def wait(seconds):
            time.sleep(seconds)
            return True
        assert wait(0.5)
        assert not wait(1.5)

    def test_make_timeout_return_value(self):
        @timeout.make_timeout(return_value = "done")
        def f():
            time.sleep(timeout.DEFAULT_TIME + 0.5)
        assert f() == "done"