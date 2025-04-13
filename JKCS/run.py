import pytest
import  os

if __name__ == '__main__':
    pytest.main(['-n 3'])
    os.system(f'allure serve ./report/temp')