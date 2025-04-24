# config.py
QQBOT_API_URL = 'http://8.138.187.179:3000'
GROUP_ID = 932411215  # 群号

# 定义一个 RSS 源列表
RSS_FEEDS = [
    {
        'TG_GROUP_NAME': 'stepleaker',
        'RSS_URL': 'https://rsshub.app/telegram/channel/stepleaker'
    },
    {
        'TG_GROUP_NAME': 'WuWaZeta',
        'RSS_URL': 'https://rsshub.app/telegram/channel/WuWaZeta'  
    },
        {
        'TG_GROUP_NAME': 'Seele',
        'RSS_URL': 'https://rsshub.app/telegram/channel/Seele_WW_Leak'  
    },

    # 可以继续添加更多的频道
]
# 抓取周期，单位为分钟
FETCH_INTERVAL = 1