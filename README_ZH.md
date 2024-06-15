<!--
 * @Description: 
 * @Author: Duke 叶兀
 * @E-mail: ljyduke@gmail.com
 * @Date: 2024-01-03 22:51:03
 * @LastEditors: Junyi_Li ljyduke@gmail.com
 * @LastEditTime: 2024-05-19 20:05:55
-->
# Agent对话网页服务

## 项目简介

本项目旨在设计一个基于Web的对话服务界面，允许用户与不同的语言模型进行交互。目前支持的服务包括百度、智谱、百川、Google和gpt等。

项目技术栈简单，python-flask+html/css/js，容易修改和扩展，适合作为实验和小规模测试使用

## 功能

- 与多个语言模型进行实时对话。
- 支持通过API Key进行身份验证。
- 支持发送和接收消息流。
- 提供简单的前端界面与后端服务进行交云。

## 安装步骤

1. 克隆项目到本地机器
   ```
   git clone git@github.com:DukeEnglish/agent_web.git
   ```
2. 进入项目目录
   ```
   cd agent_web
   ```
3. 创建并激活虚拟环境（推荐）
   ```
   python -m venv venv
   source venv/bin/activate  # 对于Windows使用 `venv\Scripts\activate`
   ```
4. 安装依赖
   ```
   pip install -r requirements.txt
   ```

## 使用方法

1. 启动后端服务
   ```
   python app.py
   ```
2. 访问`http://127.0.0.1:5000/`在浏览器中查看前端界面。

## 贡献指南

我们欢迎任何形式的贡献，请遵循以下步骤：

1. Fork 本项目。
2. 创建一个新的分支进行您的更改。
3. 提交您的更改。
4. 创建一个Pull Request。


## 联系方式

- 作者：Duke 叶兀
- 邮箱：ljyduke@gmail.com
- 微信：547160794

欢迎提出任何问题和建议！

![微信二维码](https://github.com/DukeEnglish/agent_web/blob/main/assets/per_qr_code.jpg)