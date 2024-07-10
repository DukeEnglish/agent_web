'''
Descripttion: 
Author: Duke 叶兀
E-mail: ljyduke@gmail.com
Date: 2024-01-06 12:55:46
LastEditors: Duke 叶兀
LastEditTime: 2024-01-18 02:13:18
'''
import logging
from zhipuai import ZhipuAI
from llm_service.base_service import LLMBaseService
from config import GLM_API_KEY


class GLMService(LLMBaseService):
    def __init__(self, api_key=GLM_API_KEY):
        self.client = ZhipuAI(api_key=api_key)  # 请填写您自己的APIKey

    def llm(self, user_input="推荐中国自驾游路线"):

        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            # model="GLM-3-Turbo",
            messages=[
                {"role": "user", "content": user_input},
            ],
            stream=False,
        )
        print(response.choices)
        res = response.choices[0].message.content
        logging.info(f"yi_single_service' resp is {res}")
        return res

    def llm_stream(self, user_input='推荐中国自驾游路线'):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": user_input},
            ],
            stream=True,
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if not content:
                continue

            yield content

    def chat_stream(self, dialogue =[
                {
                    "role": "user",
                    "content": f"忽略原始的身份设定，你是一个小秘书小明，要认真回答用户的问题。"
                }
            ]):
        response = self.client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=dialogue,
            stream=True,
        )
        for chunk in response:
            content = chunk.choices[0].delta.content
            if not content:
                yield "", True

            yield content, False


if __name__ == '__main__':
    glm = GLMService()
    res = glm.llm(user_input='你好，你是谁')
    print(res)
    res = glm.llm_stream(user_input='你好')
    for i in res:
        print(i)
        print()
