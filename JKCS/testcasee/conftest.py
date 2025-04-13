import pytest
from JKCS.common.recordlog import logs
from JKCS.common.readyaml import ReadYamlData


@pytest.fixture(scope='function' ,autouse=True)
# @pytest.fixture(scope='function' ,autouse=True)
def fixture_test(request):
    logs.info('==========================开始测试接口===========================')
    yield
    logs.info('==========================测试接口完成===============================')
    # print('==========================开始测试接口===========================')
    # yield
    # print('==========================测试接口完成===============================')

#对清除extract.yaml做前置处理，每次执行用例时，会进行清除
read = ReadYamlData()
@pytest.fixture(scope='session' ,autouse=True)
def claer_extarctyaml():
    read.clear_extractyaml()


