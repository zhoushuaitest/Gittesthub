import json
import pytest
import requests
from JKCS.common.recordlog import logs
from requests import utils
from JKCS.common.readyaml import ReadYamlData
class SendRequest():
    def __init__(self):
        self.read = ReadYamlData()

#封装请求方式
    def send_request(self, **kwargs):
        cookie = {}
        session = requests.session()
        result = None

        try:
            result = session.request(**kwargs)
            set_cookie = requests.utils.dict_from_cookiejar(result.cookies)
            #将ccokie写入到extract.yaml文件中
            if set_cookie:
                cookie['Cookie'] = set_cookie
                self.read.write_yaml(cookie)
                logs.info(f'cookie为 : {cookie}')
            logs.info(f'接口的实际返回信息为： : {result.text if result.text else result}')
        except requests.exceptions.ConnectionError:
            logs.error("ConnectionError--连接异常")
            pytest.fail("接口请求异常，可能是request的连接数过多或请求速度过快导致程序报错！")
        except requests.exceptions.HTTPError:
            logs.error("HTTPError--http异常")
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail("请求异常，请检查系统或数据是否正常！")
        return result

 #封装一个主函数，方便之前去调用post或者get
    def run_main(self, name, url, case_name,header, method,cookies=None,flie=None,**kwargs):

        """

                :param url: 请求地址
                :param header: 请求头
                :param data: 请求参数
                :param method: 请求方法
                :return:
                """
        # k = None
        # if method.upper() == 'GET':
        #     k = self.send_get(url,header,data)
        # elif method.upper() == 'POST':
        #     k = self.send_post(url,header,data)
        # else:
        #     print("目前只支持这几种类型")
        # return k


        try:
            # 收集报告日志信息
            logs.info('接口名称：{}'.format(name))
            logs.info('接口请求地址：{}'.format(url))
            logs.info(f'请求方法：{method}')
            logs.info(f'测试用例名称：{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'cookies：{cookies}')
            #处理请求参数,因为请求参数有data/parmas/json数据格式
            req_params = json.loads(kwargs, ensure_ascii=False)
            # kwargs = {'data': {'user_name': '${get_params()}', 'passwd': 'admin123'}}
            if 'data' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
            elif 'json' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
            elif 'params' in kwargs.keys():
                logs.info(f'请求参数：{kwargs}')
            return req_params

        except Exception as e:
            logs.error(e)
        res3 = self.send_request(method=method,url=url,headers=header,cookies=cookies, files=flie ,verify=False, **kwargs)
        return res3




        #收集报告日志信息




if __name__ == '__main__':
    url = 'http://127.0.0.1:8787/dar/user/login'

    # header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

    data = {
        "user_name": "test01",
        "passwd": "admin124443"
    }
    header =    None

    method = "post"
    #创建对象

    send = SendRequest()
    SEND = send.run_main(url=url,header=
    header,data=data,method=
    method)
    print(SEND
          )


