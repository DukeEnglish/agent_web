'''
Descripttion: 
Author: Duke 叶兀
E-mail: ljyduke@gmail.com
Date: 2024-01-06 08:55:19
LastEditors: Duke 叶兀
LastEditTime: 2024-01-08 23:30:57
'''
from llm_service.glm import GLMService
from llm_service.baichuan import BAICHUANService
from llm_service.yi import YIService
from llm_service.ernie import ERNIEService


# 工厂类
class ServiceFactory:
    _services = {
        'glm': GLMService,
        'baichuan': BAICHUANService,
        'yi': YIService,
        'ernie': ERNIEService
    }

    @staticmethod
    def get_service(service_type):
        service_cls = ServiceFactory._services.get(service_type)
        if not service_cls:
            raise ValueError(f"Unknown service type: {service_type}")
        return service_cls.get_instance()


if __name__ == '__main__':
    for i in ServiceFactory()._services.keys():
        try:
            print(f"model {i}")
            llm_client = ServiceFactory().get_service(i)
            res = llm_client.llm(user_input='你好，你是谁')
            print(res)
            # res = llm_client.llm_stream(user_input='你好')
            # for i in res:
            #     print(i)
            #     print()
        except Exception as e:
            pass
