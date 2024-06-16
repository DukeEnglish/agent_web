'''
Descripttion: 
Author: Duke 叶兀
E-mail: ljyduke@gmail.com
Date: 2024-01-06 12:55:46
LastEditors: Duke 叶兀
LastEditTime: 2024-01-18 02:13:18
'''
import logging
from llm_service.base_service import LLMBaseService
from gpt4all import GPT4All
# 难点在于下载模型，以及访问https://gpt4all.io/models/models3.json


class LocalService(LLMBaseService):
    """other model:https://gpt4all.io/index.html"""
    """如果网络无法获取model_list，需要自行修改gpt4all中获取model_list.josn的部分，示例修改如下
    gpt4all.py line 271
    try:
            resp = requests.get("https://gpt4all.io/models/models3.json")
            if resp.status_code != 200:
                raise ValueError(f'Request failed: HTTP {resp.status_code} {resp.reason}')
            return resp.json()
        except:
            import json
            with open("PATH/model_list.json") as f:
                w = json.load(f)
            return w
    
    """
    def __init__(self):

        model_name = "mistral-7b-instruct-v0.1.Q4_0.gguf"
        model_path = None
        self.client = GPT4All(model_name=model_name, model_path=model_path)
        

    def llm(self, user_input="推荐中国自驾游路线"):
        
        current_bot_output = self.client.generate(f"{user_input}", max_tokens=2000)
        return current_bot_output

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
        if not dialogue:
            # example
            dialogue = [{"role": "user", "content": "hi"},
                            {"role": "assistant", "content": "hello"},
                            {"role": "user", "content": "hi"}]
        model_input = ""
        for kv in dialogue:
            for k, v in kv.items():
                if k == "role":
                    model_input += f"{v}:"
                else:
                    model_input += f"{v}."
        print(model_input)
        current_bot_output = self.client.generate(f"{model_input}", max_tokens=200)
        yield current_bot_output
        # for chunk in response:
        #     content = chunk.choices[0].delta.content
        #     if not content:
        #         continue

        #     yield content


if __name__ == '__main__':
    glm = LocalService()
    res = glm.chat_stream()
    for i in res:
        print(i)
        print()


