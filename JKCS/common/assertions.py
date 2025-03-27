from  JKCS.common.recordlog import logs
import allure
import jsonpath
import operator
from JKCS.common.connections import ConnectMysql



class Assertions(object):
    """接口断言"""
    """
        接口断言模式，支持
        1、字符串包含
        2、结果相等断言
        3、结果不相等断言
        4、断言接口返回值中任意一个值
        5、数据库断言
        """
    # 1/字符串断言，验证接口返回数据包含在字符串中
    def contains_assert(self, value, response, status_code):
        """
        字符串包含断言
        :param expected: yaml文件里面的validation字段中的预期结果
        :param response: 接口实际返回值
        :param status_code: 接口返回的状态码
        :return:
        """
        # 断言状态标识，0成功，其他失败
        flag = 0
        for assert_key, assert_value in value.items():
            if assert_key == "status_code":
                if assert_value != status_code:
                    flag += 1
                    allure.attach(f"预期结果：{assert_value}\n实际结果：{status_code}", '响应代码断言结果:失败',
                                  attachment_type=allure.attachment_type.TEXT)
                    logs.error("contains断言失败：接口返回码【%s】不等于【%s】" % (status_code, assert_value))
            else:
                resp_list = jsonpath.jsonpath(response, "$..%s" % assert_key)
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    if isinstance(assert_value, int):
                        assert_value = assert_value
                    elif isinstance(assert_value, str):
                        assert_value = None if assert_value.upper() == 'NONE' else assert_value
                    if assert_value in resp_list:
                        logs.info("字符串包含断言成功：预期结果-->%s；实际结果-->%s" % (assert_value, resp_list))
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应文本断言结果：成功',
                                      attachment_type=allure.attachment_type.TEXT)
                    else:
                        flag = flag + 1
                        allure.attach(f"预期结果：{assert_value}\n实际结果：{resp_list}", '响应文本断言结果：失败',
                                      attachment_type=allure.attachment_type.TEXT)
                        logs.error("响应文本断言失败：预期结果为【%s】,实际结果为【%s】" % (assert_value, resp_list))
        return flag

    def equal_assert(self, expected_results, actual_results):
        """相等断言"""
        flag = 0
        res_lst = []
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            for res in actual_results:
                if list(expected_results.keys())[0] != res:
                    res_lst.append(res)
            for rl in res_lst:
                del actual_results[rl]
            eq_assert = operator.eq(actual_results, expected_results)
            if eq_assert:
                logs.info(f"相等断言成功：接口实际结果：{actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{actual_results}", '相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                logs.error(f"相等断言失败：接口实际结果{actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{actual_results}", '相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    def no_equal_assert(self, expected_results, actual_results):
        """不相等断言"""
        flag = 0
        res_lst = []
        if isinstance(actual_results, dict) and isinstance(expected_results, dict):
            for res in actual_results:
                if list(expected_results.keys())[0] != res:
                    res_lst.append(res)
            for rl in res_lst:
                del actual_results[rl]
            eq_assert = operator.ne(actual_results, expected_results)
            if eq_assert:
                logs.info(f"不相等断言成功：接口实际结果：{actual_results}，不等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{actual_results}", '不相等断言结果：成功',
                              attachment_type=allure.attachment_type.TEXT)
            else:
                flag += 1
                logs.error(f"不相等断言失败：接口实际结果{actual_results}，等于预期结果：" + str(expected_results))
                allure.attach(f"预期结果：{str(expected_results)}\n实际结果：{actual_results}", '不相等断言结果：失败',
                              attachment_type=allure.attachment_type.TEXT)
        else:
            raise TypeError('不相等断言--类型错误，预期结果和接口实际响应结果必须为字典类型！')
        return flag

    def db_assert(self,expected_sql):
        """数据库断言
        expected_sql:预期结果，也就是yaml文件的sql语句，相当于去判断新增数据后，再去查询这条数据，如果在就断言成功，不在就失败
        """
        flag = 0
        conn = ConnectMysql()
        db_value = conn.query(expected_sql)
        if db_value is not None:
            logs.info("数据库断言成功")
        else:
            flag += 1
            logs.error("数据库断言失败，请检查是否存在该数据")
        return flag

    def assert_result(self, expected, response, status_code):
        """
        断言最终封装方法
        :param expected: 预期结果，也就是yaml文件里面的validation字段的值
        :param response: 接口的实际返回结果
        :param status_code: 接口的实际返回状态码
        :return:
        """
        # 0表示接口测试成功，非0则表示接口测试失败
        all_flag = 0
        try:
            logs.info(f'yaml文件的预期结果：{expected}')
            for yq in expected:
                for key, value in yq.items():
                    if key == 'contains':
                        flag = self.contains_assert(value, response, status_code)
                        all_flag = all_flag + flag
                    elif key == 'eq':
                        flag = self.equal_assert(value, response)
                        all_flag = all_flag + flag
                    elif key == 'ne':
                        flag = self.no_equal_assert(value, response)
                        all_flag = all_flag + flag
                    elif key == 'db':
                        flag = self.db_assert(value)
                        all_flag = all_flag + flag
                    else:
                        logs.error(f'不支持{key}这种断言模式！')
        except Exception as e:
            logs.error('请检查断言字段是否包含在接口的返回值中')
            logs.error(f'异常信息：{e}')
            raise e

        if all_flag == 0:
            logs.info('测试成功')
            assert True
        else:
            logs.error('测试失败')
            assert False