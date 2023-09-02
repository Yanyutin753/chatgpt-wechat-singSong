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

@plugins.register(
    name="songSing",
    desire_priority=-1,
    hidden=False,
    desc="A plugin to sing a song",
    version="0.1",
    author="yangyang",
)
class RandomSong(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[songSing] inited")

    def on_handle_context(self, e_context: EventContext):
        content = e_context["context"].content
        if content.startswith("播放"):
            self.get_song(e_context, content[len("播放"):])
        elif content == "网易云登录":
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "\nhttps://www.yang-music.fun/qrlogin.html"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
            
        elif content == "网易云用户":
            url = "https://www.yang-music.fun/user/account"
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
        try:
            url = "https://www.yang-music.fun/search"
            params = {
                'keywords': query,
                'limit': 5
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                all_false = True  # 用于跟踪所有ID的data['message']是否都为False的标志
                for song in data['result']['songs']:
                    song_id = song['id']
                    res_url = "https://www.yang-music.fun/check/music"
                    params = {
                        'id': song_id
                    }
                    res_response = requests.get(res_url, params=params)
                    if res_response.status_code == 200:
                        data = res_response.json()
                        context = data['message']
                        if context == "ok":
                            song_url = "https://www.yang-music.fun/song/url/v1"
                            params = {
                                'id': song_id,
                                'level': "exhigh"
                            }
                            song_response = requests.get(song_url, params=params)
                            if song_response.status_code == 200:
                                song_info = song_response.json()
                                voice_url = song_info['data'][0]['url']
                                voicetest = "<a href = \"{}\">{}</a>".format(voice_url, "🎶点击播放" + query)
                                
                                # 创建回复对象并设置内容
                                reply = Reply()
                                reply.type = ReplyType.TEXT
                                reply.content = voicetest
                                
                                # 将回复对象添加到事件上下文
                                e_context["reply"] = reply
                                
                                # 设置事件动作
                                e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
                                
                                # 返回结果
                                return
                        else:
                            all_false = False  # 至少有一个ID的data['message']为True
                
                if all_false:
                    reply = Reply()
                    reply.type = ReplyType.TEXT
                    reply.content = "未找到歌曲。"
                    e_context["reply"] = reply
                    e_context.action = EventAction.BREAK_PASS
    
        except Exception as e:
            logger.error(f"获取随机歌曲失败，错误信息：{e}")
            return None


    def get_help_text(self, **kwargs):
        help_text = (
            "🥰输入 '播放 <您想听的歌曲>'，我会为播放您想听的歌曲\n"
        )
        return help_text