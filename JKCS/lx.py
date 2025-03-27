class sub():
    def __init__(self):
        pass
    def A(self):
        print(1000)
        return 100
    def B(self):
        k = self.A()
        return k


l = sub()
print(l.B())



dict01 = {}

dict01['abc'] = 100
print(dict01)







str02 = '你觉得那些纯粹你jkxnjx738232'

print(str02.index('你'))

for i in range(2):
    print(i)

from JKCS.common.readyaml import get_testcase_yaml

print('===================================')
print(get_testcase_yaml('a.yaml'))