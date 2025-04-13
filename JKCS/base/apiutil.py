
from JKCS.common.readyaml import ReadYamlData,get_testcase_yaml
import allure
from JKCS.common.debugtalk import Debugtalk

from JKCS.conf.operationConfig import OperationConfig
import jsonpath
from  JKCS.common.FZ_GET_post import SendRequest
from JKCS.common.recordlog import logs
import json
import re
from JKCS.common.assertions import Assertions

assert_res = Assertions()
class BaseRequest(object):
    def __init__(self):
        self.read = ReadYamlData()
        #读取config.ini文件
        self.conf = OperationConfig()
        #读取SendRequest中1的方法
        self.send = SendRequest()
    def replace_load(self,data):
        """
        将extract。yaml文件中的数据进行解析
        :return:
        """
        str_data =data
        #判断读取的文件数据是什么类型,如果不是就将他转成字符串
        if not isinstance(data,str):
            str_data = json.dumps(data,ensure_ascii=False)
            # print(str_data)
        # return str_data

        #用循环判断有多少个$标识的额
        for i in range(str_data.count('${')):
            if "${" in str_data and "}" in str_data:
            #index检测是否为字符串，并找到字符串的索引位置
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
            #通过找到开头和结尾的索引可以将${}取出来
                ref_startdata = str_data[start_index:end_index + 1]
            #打印出循环取出的${
                # 通过索引的方式取出函数名
                func_name = ref_startdata[2:ref_startdata.index('(')]
                #取出里面的参数值
                func_pream = ref_startdata[ref_startdata.index('(')+1 :ref_startdata.index(')')]
                #传入替换的参数获取对应的值 通过用python中的getatt,这就是反射,Debugtalk()代表对象，func_name代表函数名，(func_pream)代表传入的参数
                excract_data = getattr(Debugtalk(),func_name)(*func_pream.split(',') if func_pream else '')
                #替换解析后的完整的testcase.yaml数据
                if excract_data and isinstance(excract_data, list):
                    excract_data = ','.join(e for e in excract_data)
                str_data = str_data.replace(ref_startdata, str(excract_data))

        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    def specification_yaml(self,case_info):
        """
        规范yaml接口数据的写法
        :param case_info:指yaml文件中的2数据信息
        :return:
        """
        #接口地址
        base_url = self.conf.get_envi('host')
        # print(base_url)

        params_type = ['params' ,'data' ,'json']
        #路径
        url = base_url + case_info['baseInfo']['url']
        api_name = case_info['baseInfo']['api_name']
        method = case_info['baseInfo']['method']
        header = case_info['baseInfo']['header']
        cookie = self.replace_load(case_info['baseInfo']['cookies'])

        # 通过循环将yaml文件中testcase数据取出来
        for tc in case_info['testCase']:
            #删除case中多余的数据
            case_name = tc.pop('case_name')
            validation = tc.pop('validation')
            extract = tc.pop('extract',None)
            #获取yaml文件中为list的情况
            extract_list = tc.pop('extract_list',None)
            #判断
            for key, value in tc.items():
            #判断testcase中，数据的方式为data /paremes/json  再去调用·解析数据
                if key in params_type:
                    tc[key] = self.replace_load(value)
                    # print(tc[key])
                    # print(tc['data'])

            #再去调用请求方式
            res4 = self.send.run_main(name=api_name,url=url,case_name=case_name,flie=None,method=method,cookies=cookie,header=header,**tc)
            print(res4.text)

            allure.attach(res4.text, f'接口返回信息：{res4.text}', allure.attachment_type.TEXT)
            #将结果1转化为json格式,方便做断言1处理
            res_json = res4.json()
            #判断yaml文件中有没有extract
            try:
                if extract is not None:
                    #这步是去调用extract_data中的方法
                    self.extract_data(extract, res4.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res4.text)
            except Exception as e:
                logs.error(e)
                raise e
            #处理接口断言
            # res4.status_code为获取接口状态码
            assert_res.assert_result(validation,res_json,res4.status_code)


    def extract_data(self, testcase_extarct, response):
        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcase_extarct: testcase文件yaml中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in testcase_extarct.items():
                print(key,value)

                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                            print(extract_data)
                        self.read.write_yaml(extract_data)
                # 处理json提取参数
                if '$' in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if ext_json:
                        extarct_data = {key: ext_json}
                        logs.info('提取接口的返回值：', extarct_data)
                    else:
                        extarct_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    self.read.write_yaml(extarct_data)
        except Exception as e:
            logs.error(e)
 #当yaml文件中为所要提前数据为列表时，
    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    #传入读取所要解析的yaml文件
    res3 = BaseRequest()
    data =  get_testcase_yaml('../a.yaml')[0]
    # print(data)
    # base = BaseRequest()
    # rse = base.replace_load(data)
    # print(rse)
    res3.specification_yaml(data)
