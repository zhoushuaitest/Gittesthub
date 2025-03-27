import json

import allure
import pytest
import time
from JKCS.common.readyaml import get_testcase_yaml

from  JKCS.common.FZ_GET_post import SendRequest
import os

from JKCS.common.recordlog import logs
from JKCS.base.apiutil import BaseRequest
#优化测试报告
@allure.feature('接口关联测试')
class TestJKGL():

    # 读取用例
    # 增加报告目录机构
    @allure.story('获取商品列表数据')
    @pytest.mark.parametrize('params' , get_testcase_yaml(r'E:\Python\Python_WEB\JKCS\testcasee\proguanl\jkgl.yaml'))
    def test_case01(self,params):
        BaseRequest().specification_yaml(params)

    @allure.story('查看所关联的接口商品详情信息')
    @pytest.mark.parametrize('params', get_testcase_yaml(r'E:\Python\Python_WEB\JKCS\testcasee\proguanl\readjkgldata.yaml'))
    def test_case02(self, params):
        BaseRequest().specification_yaml(params)


if __name__ == '__main__':

    pytest.main()