# utils.py
import requests
import feedparser
import re
import datetime
import config, llm_utils  # 导入 config.py和LLM模块
import schedule
import time
import hashlib  # 用于生成消息 ID
from datetime import timezone, timedelta
import random  # 用于生成随机时间

# 用于存储已发送消息 ID 的集合
sent_message_ids = set()

# 获取当前系统时间
now = datetime.datetime.now(timezone.utc)  # 获取带时区的当前时间
# 将起始日期设置为昨天的日期
start_date = now - datetime.timedelta(days=1)

# 定义 UTC+8 时区
utc_8 = timezone(timedelta(hours=8))


def generate_message_id(entry):
    """根据条目内容生成唯一 ID"""
    # 优先使用条目的唯一 ID
    if hasattr(entry, 'id'):
        return entry.id

    # 如果没有唯一 ID，则使用链接作为 ID
    if hasattr(entry, 'link'):
        return entry.link

    # 如果以上两种方法都不可行，则结合多个字段生成 ID
    content = entry.title + entry.description + str(entry.published_parsed)
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def send_forward_message(group_id, messages, news):
    """使用转发消息接口发送消息"""
    try:
        api_url = f'{config.QQBOT_API_URL}/send_group_forward_msg'  # 替换成你的转发消息接口地址

        data = {
            "group_id": group_id,
            "messages": messages,
            "news": news,
            "prompt": "转发消息",
            "summary": f"共{len(messages)}条消息",
            "source": "来自TG群的消息"
        }
        response = requests.post(api_url, json=data)
        response.raise_for_status()
        result = response.json()

        if result['status'] == 'ok':
            print("消息转发成功")
            return True
        else:
            print("消息转发失败:", result['message'])
            return False
    except Exception as e:
        print("消息转发失败:", e)
        return False


def process_rss_feed(rss_feed):
    """处理单个 RSS Feed"""
    try:
        # 计算每个群的随机时间范围
        num_groups = len(config.RSS_FEEDS)
        random_range = 2 * config.FETCH_INTERVAL / num_groups

        # 在 0 到 random_range 分钟之间随机选择一个时间点
        delay = random.uniform(0, random_range * 60)
        print(f"等待 {delay:.2f} 秒后获取 {rss_feed['TG_GROUP_NAME']} 的 RSS 内容")  # 添加调试信息
        time.sleep(delay)

        # 使用 requests 库获取 RSS 内容
        response = requests.get(rss_feed['RSS_URL'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()
        print(f"成功获取 {rss_feed['TG_GROUP_NAME']} 的 RSS 内容")  # 添加调试信息

        # 使用 feedparser 解析 RSS 内容
        feed = feedparser.parse(response.content)

        new_messages = []
        new_news = []

        if feed.entries:  # 检查是否有条目
            print(f"{rss_feed['TG_GROUP_NAME']} 找到 {len(feed.entries)} 个条目")  # 添加调试信息
            for entry in feed.entries:
                # 获取发布时间
                if hasattr(entry, 'published_parsed'):
                    published_time = datetime.datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)  # 显式指定时区为 UTC
                    # 将 GMT 时间转换为 UTC+8 时间
                    published_time = published_time.astimezone(utc_8)
                    print(f"消息发布时间：{published_time}")  # 添加调试信息
                else:
                    print("时间获取失败，跳过该条消息")  # 添加调试信息
                    continue

                # 比较发布时间与起始日期
                if published_time < start_date:
                    print(f"消息发布时间{published_time}早于起始日期{start_date}，跳过该频道")  # 添加调试信息
                    break  # 提前跳出循环

                # 生成消息 ID
                message_id = generate_message_id(entry)

                # 检查消息是否已发送
                if message_id not in sent_message_ids:
                    # 标记为已发送
                    sent_message_ids.add(message_id)

                    description = entry.description  # 获取 description 字段的内容

                    # 提取图片链接
                    image_links = re.findall(r'<img.*?src="(.*?)"', description)

                    # 提取视频链接
                    video_links = re.findall(r'<video.*?src="(.*?)"', description)

                    # 去除 HTML 标签
                    description = re.sub(r'<[^>]+>', '', description)

                    # 格式化时间字符串
                    time_str = published_time.strftime("%Y/%m/%d %H:%M")

                    # 构建消息文本
                    text = f"【来自tg群：{rss_feed['TG_GROUP_NAME']}】\n【{time_str}】\n----------------------------\n{description}"  # 使用 description 作为消息内容

                    # 创建消息节点
                    message_node = {
                        "type": "node",
                        "data": {
                            "user_id": "菲比",  # 可以自定义
                            "nickname": "菲比",  # 可以自定义
                            "content": []
                        }
                    }

                    # 添加文本消息片段
                    text_message = {
                        "type": "text",
                        "data": {
                            "text": text
                        }
                    }
                    message_node["data"]["content"].append(text_message)

                    # 添加图片消息片段
                    for image_link in image_links:
                        image_message = {
                            "type": "image",
                            "data": {
                                "file": image_link,  # 图片文件 URL
                                "url": image_link  # 图片在线 URL
                            }
                        }
                        message_node["data"]["content"].append(image_message)

                    # 添加视频消息片段
                    for video_link in video_links:
                        video_message = {
                            "type": "video",
                            "data": {
                                "file": video_link,  # 视频文件 URL
                                "url": video_link  # 图片在线 URL
                            }
                        }
                        message_node["data"]["content"].append(video_message)

                    new_messages.insert(0, message_node)  # 将消息插入到列表的开头

                    # 构建外显文本
                    if len(new_news) < 3:  # 只添加前三条消息的外显信息
                        if image_links:
                            news_text = "菲比：【图片】"
                        elif video_links:
                            news_text = "菲比：【视频】"
                        else:
                            news_text = f"菲比：{text}"
                        new_news.append({"text": news_text})

            # 对 news 列表进行倒序排列
            new_news.reverse()

            return new_messages, new_news

        else:
            print(f"{rss_feed['TG_GROUP_NAME']} 没有找到任何条目呢！")  # 添加调试信息
            return [], []

    except requests.exceptions.RequestException as e:
        print(f"获取 {rss_feed['TG_GROUP_NAME']} 的 RSS 内容时发生网络请求错误:", e)  # 添加调试信息
        return [], []
    except Exception as e:
        print(f"处理 {rss_feed['TG_GROUP_NAME']} 的 RSS 内容时发生错误:", e)  # 添加调试信息
        return [], []


def process_all_rss_feeds():
    """处理所有 RSS Feed"""
    print(f"开始处理所有 RSS Feed，当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")  # 添加调试信息
    all_messages = []
    all_news = []
    # 先处理所有的 RSS 源，生成消息列表
    for rss_feed in config.RSS_FEEDS:
        messages, news = process_rss_feed(rss_feed)
        all_messages.extend(messages)
        all_news.extend(news)
        
    if config.is_LLM:
        all_messages = fix_messages_format(all_messages)
    else:
        print("LLM 已关闭，跳过消息格式修复")  # 调试信息
    # 只保留 all_news 的前三条
    all_news = all_news[:3]
    # 循环处理每个群聊，发送相同的消息列表
    for group in config.GROUPS:
        group_id = group['GROUP_ID']
        group_name = group['GROUP_NAME']
        if all_messages:
            # 发送消息到 QQ 群
            print(f"准备向 {group_name} 发送消息")  # 调试信息
            send_forward_message(group_id, all_messages, all_news)
        else:
            print(f"{group_name} 没有新消息呢！")  # 调试信息
    print(f"处理 RSS Feed 结束，当前时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")  # 调试信息
    print("等待下一次轮询开始......")
def fix_messages_format(messages):
    """使用 LLM 修复消息列表中的文本格式"""
    formatted_messages = []
    for message in messages:
        if message["type"] == "node":
            print("处理消息节点")  # 调试信息
            for content in message["data"]["content"]:
                if content["type"] == "text":
                    print("处理文本内容")  # 调试信息
                    # 调用 LLM 修复文本格式
                    try:
                        time.sleep(config.req_interval)  # 添加 sleep，单位为秒，可以根据需要调整
                        content["data"]["text"] = llm_utils.generate_gemini_response(content["data"]["text"])
                        print("LLM处理成功")  # 调试信息
                    except Exception as e:
                        print(f"LLM处理失败: {e}")  # 调试信息
        formatted_messages.append(message)  
        return formatted_messages


def scheduled_task():
    """定时执行的任务"""
    process_all_rss_feeds()
