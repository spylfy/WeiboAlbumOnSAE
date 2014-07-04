WeiboAlbumOnSAE
===

这是一个可以将 weibo 改造成图床的工具，可以运行在 SAE 上。

简单部署
---

1. 下载本项目[代码包](https://github.com/Sandtears/WeiboAlbumOnSAE/archive/master.zip)
2. 创建 SAE 应用，开发语言选择 Python
3. 创建微博开放平台应用，并将 OAuth 授权回调地址设置为
`http://[yourappname].sinaapp.com/access_token.html`
4. 将开放平台应用的 AppKey，AppSecret 和授权回调地址填入 `config.py` 中，并将项目上传至 SAE。
5. 访问 `http://[yourappname].sinaapp.com/`，获取 `access_token` 并填入 `config.py`
6. 再次 `http://[yourappname].sinaapp.com/`，填写预设密码即可。

设置说明
---

设置文件 `config.py` 中的 `params` 代表上传参数，默认情况下发送的微博仅密友可见，更多关于 `params` 参数的信息可以访问[微博开放平台文档](http://open.weibo.com/wiki/2/statuses/upload)获取。