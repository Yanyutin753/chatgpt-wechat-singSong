# chatgpt-wechat-网易云音乐播放插件

这是一个用于在你的应用中播放网易云音乐的插件，它利用网易云音乐的API实现了多种功能，包括播放指定音乐、用户登录以及VIP音乐的支持。你还可以根据[网易云api](https://neteasecloudmusicapi.vercel.app/#/)，自行拓展更多功能。

## 功能特性
- 调用自己部署的[网易云音乐的API](https://github.com/Binaryify/NeteaseCloudMusicApi)
- 播放指定音乐：通过调用网易云音乐的API，你可以输入音乐ID或链接来播放指定的音乐。
- 用户登录：支持用户登录功能，使用户可以登录自己的网易云音乐账号。
- VIP音乐支持：一旦用户登录，插件将允许播放VIP音乐，让用户畅享更多高质量音乐。
- 开发者友好：你可以根据网易云音乐的API文档，自行开发更多功能，比如获取歌曲信息、创建播放列表等。

## 安装与使用

1. 部署[网易云音乐的API](https://github.com/Binaryify/NeteaseCloudMusicApi)（推荐Vercel部署，具体可阅读[详细文档](https://github.com/Binaryify/NeteaseCloudMusicApi))
1. 下载插件并将其添加到你的plugins文件夹中。
2. 根据提供的示例代码，修改[singSong.py]里的接口地址，实现各种功能。

## 登录
登录的方式有三种：
一是管理员登录，在godcmd插件添加相应的代码。[具体可参考下面文档]([https://github.com/Binaryify/NeteaseCloudMusicApi](https://github.com/Yanyutin753/chatgpt-wechat-/blob/main/%E7%BD%91%E6%98%93%E9%9F%B3%E4%B9%90/godcmd.py.temp))
二是输入登录，扫描二维码进行登录。
三是浏览器访问你们部署的网站加/qrlogin.html，进行登录
按照你们的需求，自行修改代码实现登录

##使用情况

![505d3ec6fbdce237d3619ca2854db18](https://github.com/Yanyutin753/chatgpt-wechat-singSong/assets/132346501/27017915-1d7c-4413-a8fe-b04cc2c3b652)

![3372ce45d0d01c9c8d2bdd1d832e943](https://github.com/Yanyutin753/chatgpt-wechat-singSong/assets/132346501/794c3699-5e8d-45f9-96df-5f01bfcf45a0)

![70eaa417c9b3cc6e3cc668f0b53feea](https://github.com/Yanyutin753/chatgpt-wechat-singSong/assets/132346501/29000ddf-db40-4948-aef6-85ff0129ba09)


## 贡献与支持
欢迎贡献代码，提出问题和建议。如果你发现了bug或者有新的功能想法，请提交一个Issue让我知道。你也可以通过Fork项目并提交Pull Request来贡献代码。
如果你喜欢这个项目，欢迎给它一个星星⭐，这是对我最大的支持！
