'''
Descripttion: 
Author: Duke 叶兀
E-mail: ljyduke@gmail.com
Date: 2024-01-06 12:55:46
LastEditors: Duke 叶兀
LastEditTime: 2024-01-18 02:13:18
'''
from config import BAICHUAN_API_KEY
from llm_service.base_service import LLMBaseService


import requests
import json


class BAICHUANService(LLMBaseService):
    """
    LLM模型基础服务 baichuan
    """

    def __init__(self):
        """
        url = "https://api.baichuan-ai.com/v1/chat/completions"
        """
        self.url = "https://api.baichuan-ai.com/v1/chat/completions"
        self.api_key = BAICHUAN_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }
        self.data = {
            "model": "Baichuan2-Turbo",
            "stream": False
        }

    def llm(self, user_input="推荐中国自驾游路线"):
        self.data["messages"] = [
            {
                "role": "user",
                "content": f"{user_input}"
            }
        ]
        json_data = json.dumps(self.data)
        response = requests.post(
            self.url, data=json_data, headers=self.headers, timeout=60, stream=True)
        print(response)

    def llm_stream(self, user_input="推荐中国自驾游路线"):
        self.data["stream"] = True
        self.data["messages"] = [
            {
                "role": "user",
                "content": f"{user_input}"
            }
        ]
        json_data = json.dumps(self.data)
        response = requests.post(
            self.url, data=json_data, headers=self.headers, timeout=60, stream=True)
        print(response)


if __name__ == '__main__':
    llm_client = BAICHUANService(BAICHUAN_API_KEY)
    res = llm_client.llm(user_input='你好，你是谁')
    print(res)
    res = llm_client.llm_stream(user_input='你好')
    for i in res:
        print(i)
        print()
