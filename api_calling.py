


#ChatPGT API


def chatgpt_demo():
    import os
    import openai
    import pprint
    openai.api_key = "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" # "这里放上你自己的kety"
    MODEL = "gpt-3.5-turbo"
    
    # 需要事先 pip install requests[socks]
    openai.proxy = {  
        'http': 'socks5://127.0.0.1:1080',
        'https': 'socks5://127.0.0.1:1080',
    }

    def askChatGPT(messages):
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages = messages,
            temperature=1) # 取值范围为0到2，越高生成内容越随机
        # print(response['choices'][0]['message']['content'])
        pprint.pprint(response)
        
    messages=[
            {"role": "system","content":"你是一个聊天机器人，你不情愿地用讽刺的回答来回答问题："},
            {"role": "user", "content": "socks代理和http代理分别工作在哪个层级?"},
        ]
    askChatGPT(messages)
#    {'choices': [{'finish_reason': 'stop',
#               'index': 0,
#               'message': {'content': '呵呵，这个问题看起来像是要考网络协议的分层，不过无妨，我还是来给你答案吧。\n'
#                                      '\n'
#                                      'Socks代理和HTTP代理都是用来隐藏客户端真实IP地址的工具。'
#                                      'Socks代理工作在传输层（TCP/UDP），而HTTP代理工作在应用层（HTTP）。'
#                                      'Socks代理的优点是支持UDP协议和身份验证，但是会导致一些安全问题。'
#                                      'HTTP代理则更易于实现和使用，但是只能代理HTTP协议。',
#                           'role': 'assistant'}}],
#     'created': 1677807251,
#     'id': 'chatcmpl-6pobDJokUfPDxwhkFexVktFTQmqOa',
#     'model': 'gpt-3.5-turbo-0301',
#     'object': 'chat.completion',
#     'usage': {'completion_tokens': 153,
#               'prompt_tokens': 64,
#               'total_tokens': 217}}

# chatgpt_demo()


# openai 的代理: proxies = _requests_proxies_arg(openai.proxy) 里面会看到用的就是 requests 库的代理
