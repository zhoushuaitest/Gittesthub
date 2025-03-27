from JKCS.common.readyaml import ReadYamlData
import random
#获取extracrt.yaml文件中的数据，进行testcase.yaml文件动态读取
class Debugtalk:
    def __init__(self):
        self.read = ReadYamlData()

    def get_ex_data_list(self, node_name,randoms=None):

        data = self.read.read_extract_yaml(node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: 1,
                0: random.choice(data),
                -1: ','.join(data),
            }
            data = data_value[randoms]
        return data


    def get_ex_data(self, node_name,sec_node_name=None,randoms=None):

        data = self.read.read_extract_yaml(node_name,sec_node_name)
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: 1,
                0: random.choice(data),
                -1: ','.join(data),
            }
            data = data_value[randoms]
        return data


    #参数md5加密
    def md5_parme(self,parme):
        return 'admin12345' + str(parme)

if __name__ == '__main__':
    debugtalk = Debugtalk()
    rse_extractyaml = debugtalk.get_ex_data('token')
    print(rse_extractyaml)



