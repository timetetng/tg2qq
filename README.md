# tg2qq

## 简介

这是一个小巧可爱的 Python 脚本，可以将 Telegram 频道的消息转发到 QQ 机器人（Napcat）。它通过 Napcat 的 HTTP 请求接口实现，支持订阅 Telegram 频道的文本、图片和视频，然后将它们转发到指定的 QQ 群里哦！

## 特点

*   **简单易用**：配置简单，运行方便，像菲比一样好上手呢！
*   **多媒体支持**：支持转发文本、图片和视频消息，内容丰富多彩！
*   **定时轮询**：可以设置定时轮询周期，自动获取最新消息并转发。
*   **消息去重**：可以自动过滤已发送的消息，避免重复发送。
*   **自定义消息格式**：可以自定义转发消息的格式，让消息更可爱！

## 文件结构

```
tg2qq/
├── config.py          # 配置文件
├── utils.py           # 主函数
├── main.py            # 主程序
├── requirements.txt   # 依赖文件
└── README.md          # 就是这份说明文件啦！
```

*   `config.py`: 配置文件，用于配置订阅的 Telegram 频道、QQ 群 ID、QQ 机器人 HTTP 接口地址、轮询周期等信息。
*   `utils.py`: 包含主要功能的函数，例如获取 RSS 内容、解析消息、发送消息等。
*   `main.py`: 主程序入口，负责启动定时任务。
*   `requirements.txt`: 包含项目依赖的 Python 库列表。

## 安装步骤

1.  **安装 Python 3**：确保您的电脑上安装了 Python 3 环境。
2.  **安装依赖库**：使用 pip 安装 `requirements.txt` 中列出的依赖库。

    ```bash
    pip install -r requirements.txt
    ```

3.  **配置 config.py**：根据您的实际情况修改 `config.py` 文件。

    ```python
    # config.py
    QQBOT_API_URL = '你的 QQ 机器人 HTTP API 地址'
    GROUP_ID = 你的 QQ 群 ID

    # 定义一个 RSS 源列表
    RSS_FEEDS = [
        {
            'TG_GROUP_NAME': 'Telegram 频道名称',
            'RSS_URL': 'Telegram 频道 RSS 地址'
        },
        # 可以继续添加更多的频道
    ]
    # 抓取周期，单位为分钟
    FETCH_INTERVAL = 1
    ```

4.  **运行 main.py**：在命令行中运行 `main.py` 启动脚本。

    ```bash
    python main.py
    ```

## 配置说明 (config.py)

*   `QQBOT_API_URL`: QQ 机器人 HTTP API 的地址。请替换为您的实际地址。
*   `GROUP_ID`: 要接收转发消息的 QQ 群 ID。请替换为您的实际群 ID。
*   `RSS_FEEDS`: 一个列表，包含要订阅的 Telegram 频道的信息。每个频道的信息是一个字典，包含以下键：
    *   `TG_GROUP_NAME`: Telegram 频道的名称，用于在转发消息中显示。
    *   `RSS_URL`: Telegram 频道的 RSS 地址。
*   `FETCH_INTERVAL`: 轮询周期，单位为分钟。脚本会每隔 `FETCH_INTERVAL` 分钟检查一次 Telegram 频道是否有新消息。

## 使用说明

1.  **获取 Telegram 频道 RSS 地址**：
    *   您可以使用第三方服务将 Telegram 频道转换为 RSS 源。例如，可以使用 RSSHub (推荐) 或者 TelegamToRss (可能需要魔法)。
2.  **配置 QQ 机器人**：
    *   确保您已经安装并配置好了 Napcat QQ 机器人，并且开启了 HTTP API 接口。
3.  **运行脚本**：
    *   配置好 `config.py` 文件后，运行 `main.py` 脚本，它会自动开始轮询 Telegram 频道并将消息转发到 QQ 群。

## 注意事项

*   确保您的 QQ 机器人能够正常接收和发送消息。
*   请勿滥用此脚本，遵守相关法律法规和平台规定。
*   如果遇到问题，可以查看日志输出，或者向菲比提问哦！

## 感谢

感谢您使用这个小脚本！希望它能给您带来便利和快乐！
