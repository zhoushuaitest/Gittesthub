import pytest
import time


class Testdetect():
    def test_delect1(self):
        time.sleep(2)
        print("测试delect1")

    time.sleep(2)
    # @pytest.mark.delect
    # @pytest.mark.skip
    def test_delect2(self):
        time.sleep(2)
        print("测试delect2")

# if __name__ == '__main__':
#     pytest.main()