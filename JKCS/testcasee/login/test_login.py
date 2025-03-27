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
@allure.feature('登录接口')
class Testlogin():

    # 读取用例
    # 增加报告目录机构
    @allure.story('用户登录正确验证')
    @pytest.mark.parametrize('params' , get_testcase_yaml(r'E:\Python\Python_WEB\JKCS\testcasee\login\login02.yaml'))
    def test_case01(self,params):
        BaseRequest().specification_yaml(params)

    @allure.story('新增用户')
    @pytest.mark.parametrize('params', get_testcase_yaml(r'E:\Python\Python_WEB\JKCS\testcasee\login\adddata.yaml'))
    def test_case02(self, params):
        BaseRequest().specification_yaml(params)


if __name__ == '__main__':

    pytest.main()