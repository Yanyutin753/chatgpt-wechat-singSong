import plugins
import requests
import re
import json
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from pydub import AudioSegment
from channel import channel
from common.log import logger
from plugins import *
from PIL import Image
from common.tmp_dir import TmpDir
import urllib.request
import urllib.parse
import os

@plugins.register(
    name="singsong",
    desire_priority=91,
    hidden=False,
    desc="A plugin to sing a song",
    version="0.1",
    author="yangyang",
)
class singsong(Plugin):
    def __init__(self):
        super().__init__()
        try:
            conf = super().load_config()
            if not conf:
                raise Exception("config.json not found")
            self.api_url = conf["api_url"]
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            logger.info("[singsong] inited")
        except Exception as e:
            logger.warning("[singsong] init failed, ignore ")
            raise e
        
    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        content = e_context["context"].content
        if content.startswith("播放"):
            logger.info(f"[singsong] {content}")
            self.get_song(e_context, content[len("播放"):])
        elif content == "网易云登录":
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = f"{self.api_url}/qrlogin.html"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
            
        elif content == "网易云用户":
            url = f"{self.api_url}/user/account"
            # 发送GET请求获取网页内容
            response = requests.get(url)
            # 检查响应状态码
            reply = Reply()
            replytext = ""
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data is not None and data['profile'] is not None:
                        replytext += f"🤖用户名: {data['profile']['nickname']}"
                        replytext += f"🧸用户id: {data['profile']['userId']}"
                        replytext += f"👑VIP类型: {data['account']['vipType']}"
                    else:
                        replytext += "😭请检查您是否登录账户"
                except (KeyError, ValueError):
                    replytext += "😭无法解析服务器返回的数据"
                    reply.type = ReplyType.TEXT
                    reply.content = replytext
                    e_context["reply"] = reply
                    e_context.action = EventAction.BREAK_PASS
            else:
                replytext += "😭网络出问题了..."
            reply.type = ReplyType.TEXT
            reply.content = replytext
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS

    def get_song(self, e_context, query):
        def is_song_available(song_id):
            check_url = f"{self.api_url}/check/music"
            check_params = {
                'id': song_id,
            }
            check_response = requests.get(check_url, params=check_params)
            if check_response.status_code == 200:
                data = check_response.json()
                context = data.get('message')
                if context == "ok":
                    logger.info(f"[singsong] Music ID：{song_id} 可用")
                    return True
            return False
    
        def download_song(query, song_id):
            reply = Reply()
            song_url = f"{self.api_url}/song/url/v1"
            download_params = {
                'id': song_id,
                'level': "exhigh",
            }
            song_response = requests.get(song_url, params=download_params)
            if song_response.status_code == 200:
                song_info = song_response.json()
                voice_url = song_info["data"][0]["url"]

                
                # 企业微信无法转化音乐为单音道，且转化之后音质很差，于是可以想着发送超链接
                # voicetest = "<a href = \"{}\">{}</a>".format(voice_url, "🎶点击播放" + query)
                # # 创建回复对象并设置内容
                # reply = Reply()
                # reply.type = ReplyType.TEXT
                # reply.content = voicetest
                # # 将回复对象添加到事件上下文
                # e_context["reply"] = reply
                # 发送MP3文件，可以使用除了企业微信之外的部署方式

                
                file_name = query + ".mp3"
                file_path = os.path.join("tmp", file_name)
                try:
                    if not os.path.exists("tmp"):  # 检查 "tmp" 目录是否存在，如果不存在则创建
                        os.makedirs("tmp")
                    with urllib.request.urlopen(voice_url) as response, open(file_path, 'wb') as out_file:
                        out_file.write(response.read())
                    logger.info(f"[singsong] Music ID：{song_id} 下载成功, {voice_url}")
                    reply.type = ReplyType.VOICE
                    reply.content = file_path
                except Exception as e:
                    logger.error(f"[singsong] Music ID：{song_id} 下载错误, {voice_url}")
            return reply
        
        url = f"{self.api_url}/search"
        search_params = {
            'keywords': query,
            'limit': 10
        }
        search_result = requests.get(url, params=search_params)
        if search_result.status_code == 200:
            data = search_result.json()
            if data['result']['songCount'] == 0:
                reply = Reply()
                reply.type = ReplyType.TEXT
                reply.content = "未找到歌曲。"
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                for song in data['result']['songs']:
                    song_id = song['id']
                    if is_song_available(song_id):
                        reply = download_song(query, song_id)
                        e_context["reply"] = reply
                        e_context.action = EventAction.BREAK_PASS
                        return
                    else:
                        reply = Reply()
                        reply.type = ReplyType.TEXT
                        reply.content = "版权问题，无法播放。"
                        e_context["reply"] = reply
                        e_context.action = EventAction.BREAK_PASS

        else:
            logger.info(f"[singsong] 服务器错误")
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "服务器错误。"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
            return None

    def get_help_text(self, **kwargs):
        help_text = (
            "🥰输入 '播放 <您想听的歌曲>'，我会为播放您想听的歌曲\n"
        )
        return help_text
