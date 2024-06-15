<!--
 * @Description: 
 * @Author: Duke Ye Wu
 * @E-mail: ljyduke@gmail.com
 * @Date: 2024-01-03 22:51:03
 * @LastEditors: Junyi_Li ljyduke@gmail.com
 * @LastEditTime: 2024-05-19 20:05:55
-->
# Agent Dialogue Web Service

## Project Introduction

This project aims to design a web-based dialogue service interface that allows users to interact with various language models. Currently supported services include Baidu, Zhishu, Baichuan, Google, and GPT, among others.

The project's technology stack is simple, using python-flask combined with HTML/CSS/JS, making it easy to modify and extend, suitable for experimental and small-scale testing use.

## Features

- Real-time dialogue with multiple language models.
- Support for identity authentication via API Key.
- Support for sending and receiving message streams.
- Provides a simple front-end interface for interaction with the back-end service.

## Installation Steps

1. Clone the project to the local machine
   ```
   git clone git@github.com:DukeEnglish/agent_web.git
   ```
2. Enter the project directory
   ```bash
   cd agent_web
   ```
3. Create and activate a virtual environment (recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
   ```
4. Install dependencies
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the back-end service
   ```
   python app.py
   ```
2. Visit `http://127.0.0.1:5000/` to view the front-end interface in the browser.

## Contribution Guidelines

We welcome contributions in any form, please follow these steps:

1. Fork this project.
2. Create a new branch for your changes.
3. Commit your changes.
4. Create a Pull Request.

## Contact Information

- Author: Duke Ye Wu
- Email: ljyduke@gmail.com
- WeChat: 547160794

Please feel free to raise any issues or suggestions!

![WeChat QR Code](https://github.com/DukeEnglish/agent_web/blob/main/assets/per_qr_code.jpg)