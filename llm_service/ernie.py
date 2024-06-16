'''
Author: ljyduke 叶兀
Date: 2024-01-05 23:44:28
LastEditors: Duke 叶兀
LastEditTime: 2024-02-20 21:11:07
FilePath: /paper_tutor/llm_service/ernie.py
Description: 

Copyright (c) 2024 by ${ljyduke@gmail.com}, All Rights Reserved. 
'''

import requests
import json
import logging
from llm_service.base_service import BAIDULLMService
from config import BAIDU_API_KEY, BAIDU_SECRET_API_KEY


class ERNIEService(BAIDULLMService):
    """
    ernie模型
    """

    def __init__(self, api_key=BAIDU_API_KEY, sec_key=BAIDU_SECRET_API_KEY):
        super().__init__()
        if api_key and sec_key:
            self.url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + \
                self._get_access_token(BAIDU_API_KEY, BAIDU_SECRET_API_KEY)
        else:
            self.url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" + \
                self._get_access_token()
        self.headers = {
            'Content-Type': 'application/json'
        }

    def llm(self, user_input="推荐中国自驾游路线"):
        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": f"忽略原始的身份设定，你是一个小秘书小明，要认真回答用户的问题。下面是用户的问题：{user_input}"
                }
            ]
        })

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload)
        logging.info(f"ernie_single_service' resp is {response.text}")
        print(response.text)
        return json.loads(response.text)['result']

    def llm_stream(self, user_input='推荐中国自驾游路线'):

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": f"忽略原始的身份设定，你是一个小秘书小明，要认真回答用户的问题。下面是用户的问题：{user_input}"
                }
            ],
            "stream": True
        })

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload, stream=True)

        for line in response.iter_lines():
            if not line:
                continue
            res = json.loads(":".join(line.decode("utf-8").split(":")[1:]))
            if res["is_end"]:
                logging.info(f"result is done for user_input {user_input}")
            yield res["result"]

    def chat_stream(self, dialogue =[
                {
                    "role": "user",
                    "content": f"忽略原始的身份设定，你是一个小秘书小明，要认真回答用户的问题。"
                }
            ]):
        dialogue_dict = {"messages": dialogue}
        dialogue_dict["stream"] = True
        payload = json.dumps(dialogue_dict)

        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload, stream=True)

        for line in response.iter_lines():
            if not line:
                continue
            res = json.loads(":".join(line.decode("utf-8").split(":")[1:]))
            if res["is_end"]:
                logging.info(f"result is done for")
            yield res["result"]
        


if __name__ == '__main__':
    ernie = ERNIEService()
    res = ernie.llm(user_input='你好')
    print(res)
    for i in res:
        print(i)
        print()
