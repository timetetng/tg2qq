# config.py
QQBOT_API_URL = 'http://' #Napcat HTTP服务器URL
# 定义一个群聊列表
GROUPS = [
    {
        'GROUP_NAME': '群聊1',
        'GROUP_ID': xxxxxxxx  # 群号
    },
    {
        'GROUP_NAME': '群聊2',
        'GROUP_ID': xxxxxxxx  # 群号
    },
    # 可以继续添加更多的群聊
]
# 定义一个 RSS 源列表
RSS_FEEDS = [
    {
        'TG_GROUP_NAME': 'xxx',
        'RSS_URL': 'https://rsshub.app/telegram/channel/xxx'
    },
    {
        'TG_GROUP_NAME': 'yyy',
        'RSS_URL': 'https://rsshub.app/telegram/channel/yyy'  
    },
        {
        'TG_GROUP_NAME': 'zzz',
        'RSS_URL': 'https://rsshub.app/telegram/channel/zzz'  
    },

    # 可以继续添加更多的频道
]
# 抓取周期，单位为分钟
FETCH_INTERVAL = 10

# 是否使用LLM格式化 (默认关闭)
is_LLM = False
# LLM 请求间隔，单位为秒
req_interval = 3
# 以gemini为例，若使用其他LLM服务商，修改下面API_KEY配置以及llm_utils.py调用代码即可
# Gemini API Key
API_KEY = "你的API_KEY"
# 模型
MODEL_NAME = 'models/gemini-2.0-flash'
# 系统提示词，可根据需求调整，比如添加双语翻译
SYSTEM_PROMPT = """
你是一个文本格式化工具，你的任务是修复给定文本中的格式问题，例如：
- 修复不正确的缩进
- 修复不正确的换行
- 移除多余的空格
- 确保文本清晰易读
下面是一些要求：
如遇到形如："Image_563099568650661.png
Image_563183155179588.png 3.9 MB"的文本，说明该图片无法获取，替换为”【无法获取图片 xx MB（如果有大小）】“即可,对于某消息含有“Video is too big”说明此处有视频过大无法爬去，同样替换为“【视频过大无法获取】”
请保持文本的原始结构和内容不变，只修复格式问题，如果用户本次没有输入或没有待格式化/翻译内容，则返回原文即可。
"""
