import plugins
import requests
import re
import json
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel import channel
from common.log import logger
from plugins import *
from PIL import Image
from common.tmp_dir import TmpDir
import urllib.request

@plugins.register(
    name="songSing",
    desire_priority=-1,
    hidden=True,
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
        if content.startswith("播放 "):
            self.get_song(e_context, content[len("播放 "):])

    def get_song(self,e_context, query):
        try:
            url = "https://service-r4ko3cqs-1317580351.gz.apigw.tencentcs.com/release/search"
            params = {
                'keywords': query,
                'limit': 1
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                first_id = data['result']['songs'][0]['id']
                res_url = "https://service-r4ko3cqs-1317580351.gz.apigw.tencentcs.com/release/check/music"
                params = {
                    'id': first_id
                }
                res_response = requests.get(res_url, params=params)
                if res_response.status_code == 200:
                    reply = Reply()
                    data = res_response.json()
                    context = data['message']
                    if context == "ok":
                        song_url = "https://service-r4ko3cqs-1317580351.gz.apigw.tencentcs.com/release/url/v1"
                        params = {
                            'id': first_id,
                            'level': "exhigh"
                        }
                        song_response = requests.get(song_url, params=params)
                        if song_response.status_code == 200:
                            song_info = song_response.json()
                            reply.type = ReplyType.VOICE
                            voice_url = song_info['data'][0]['url']
                            fileName = TmpDir().path() + query + ".mp3"
                            try:
                                urllib.request.urlretrieve(voice_url, fileName)
                                print("文件下载成功")
                            except Exception as e:
                                print("文件下载出错:", e)
                            reply.content = fileName
                            e_context["reply"] = reply
                            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
                    else:
                        reply = Reply()
                        reply.type = ReplyType.TEXT
                        reply.content = context
                        e_context["reply"] = reply
                        e_context.action = EventAction.BREAK_PASS
                        
        except Exception as e:
            logger.error(f"get_Randomsong失败，错误信息：{e}")
            return None

    def get_help_text(self, **kwargs):
        help_text = (
            "🥰输入 '播放 <您想听的歌曲>'，我会为播放您想听的歌曲\n"
        )
        return help_text
