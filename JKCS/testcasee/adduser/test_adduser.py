import pytest
import time


class TestAddUser():
    def test_add_user(self):
        time.sleep(2)
        print("测试aduser")

    # @pytest.mark.adduser
    # @pytest.mark.skip
    def test_add_user2(self):
        time.sleep(2)
        print("测试aduser02")

# if __name__ == '__main__':
#     pytest.main()