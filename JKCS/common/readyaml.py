import json
import  os
import yaml
from JKCS.conf.setting import FILE_PATH
from JKCS.common.recordlog import logs



def get_testcase_yaml(file):
    try:
        with open(file, 'r',encoding='utf-8') as f:
            yaml_read = yaml.safe_load(f.read())
            return yaml_read

    except Exception as e:
        print(e)


#将读取的数据写入到yaml中
class ReadYamlData:
    def __init__(self,yaml_file= None):
        if yaml_file is not None:
            self.yaml_file = yaml_file
        else:
            self.yaml_file = 'login.yaml'

    def write_yaml(self,value):
        """

        :param value: 写入的数据·
        :return:
        """
        #创建一个需要写入的文件
        try:
            #这个文件为setting.py中的文件路径
            file_path = FILE_PATH['EXTRACT']
            #将这个文件先打开，再进行写入
            with open(file_path,'a',encoding='utf-8') as f:
                #判断写入的文件是否为字典，如果不是字典，则提示
                if isinstance(value,dict):
            #将要写入的VALUE,进行写入加入allow_unicode=True表示可以写入中文
                    yaml_write = yaml.dump(value,allow_unicode=True)
                    f.write(yaml_write)
                else:
                    print('写入到【extract.yaml】文件中的格式必须为字典')
        except Exception as e:
            print(e)

#获取extract.yaml文件中数据，如token进行读取出来，方便面做参数动态读取

    def read_extract_yaml(self,node_name, second_node_name=None):


        """
        读取extracr.yaml文件中的数据
        :param node_name:
        :return:
        """

        if os.path.exists(FILE_PATH['EXTRACT']):
            pass
        else:
            logs.error('extract.yaml不存在')
            file = open(FILE_PATH['EXTRACT'], 'w')
            file.close()
            logs.info('extract.yaml创建成功！')
        try:
            with open(FILE_PATH['EXTRACT'], 'r', encoding='utf-8') as rf:
                ext_data = yaml.safe_load(rf)
                if second_node_name is None:
                    return ext_data[node_name]
                else:
                    return ext_data[node_name][second_node_name]
        except Exception as e:
            logs.error(f"【extract.yaml】没有找到：{node_name},--%s" % e)



    def clear_extractyaml(self):
        """

        :return: 清楚extract文件数据
        """
        with open(FILE_PATH['EXTRACT'], 'w', encoding='utf-8') as f:
            #文件清除操作
            f.truncate()


if __name__ == '__main__':
    # get_testcase_yaml('../a.yaml')
    # #读取YAMl文件
    # print('=================================')
    #
    # print(get_testcase_yaml('../a.yaml'))
    # res = get_testcase_yaml('../a.yaml')[0]
    # print(res)
    # #获取yaml文件中的url
    # url =res['baseInfo']['url']
    # new_url = 'http://127.0.0.1:8787' + url
    # #获取yaml中的data
    # data2 = res['testCase'][0]['data']
    # #获取yaml中的header
    # headers = res['baseInfo']['header']
    # #获取yaml中method
    # method = res['baseInfo']['method']
    #
    # from FZ_GET_post import SendRequest
    # send = SendRequest()
    # res = send.run_main(url=new_url, method=method,header=headers,data=data2,name=None,case_name=None)
    # print(res)
    # #通过反序列化将STR变为JSON
    # token_res = json.loads(res)
    # token = token_res.get('token')
    # print(token)
    # print('==============')


    #实例化对象，将读取的token写入到yaml文件中

    write_yaml = ReadYamlData()

    #定义一个空字典，将获取的token已字典的方式传入
    # dict_write = {}
    # dict_write['token'] = token
    # print(dict_write)
    # #将获取的数据进行写入到extarc.yaml中
    # print(write_yaml.write_yaml(dict_write))
    # print('===========')

    # 获取extract.yaml文件中数据
    RES = write_yaml.read_extract_yaml('goodsId' ,0)
    print(RES)




