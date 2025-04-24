# config.py
QQBOT_API_URL = 'http://' #Napcat HTTP服务器URL
GROUP_ID = xxxx  # 群号

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
