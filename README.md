# 一个爬取视频的项目

---

### `ffmpeg`版本 6.0
### `python`版本 python3.10

---

## 一. 介绍
1. 一个视频下载项目
2. 地址（b64解码）
```bash
aHR0cHM6Ly81NTVkeXgzLmNvbS92b2RwbGF5LzQyMTAyNC0yLTEuaHRtbA==
```
3. 项目用的`aiohttp`异步库发生请求
4. 本项目的难点是过无限`debugger`，需要手动去源码过定时器和条件分支，不然浏览器点一律不在此处执行会有内存爆破，浏览器会卡死
5. 视频下载地址在`m3u8`文件里面，需要`AES-128`解密。下载的文件是`ts`，需要合并
6. 用`ffmpeg`命令行工具合并，下载后需要添加到环境变量,不然程序下载完成后`ts`文件合并的时候会报错
```bash
https://ffmpeg.p2hp.com/download.html#build-windows
```
7. 代码运行完毕后，需要等待一会儿视频才可以打开
8. `m3u8`文件地址需要先在主页里面找到是哪一个路线的，然后用`xpath`拿到`sid`，去请求另一个地址，得到一个字典，里面包含`url`，是一个加密的，无法解密。这个密文数据是`AES`加密后放在请求头中的数据,请求头有`AES`、`MD5`、`HmacSha256`等方式加密的四个请求头，还有四个`md5`的参数加密。请求这个地址得到一个`AES`加密的字符串，解密后`json`转换为字典，得到`m3u8`文件的真正下载地址

---


## 二. 使用
1. 下载项目
```bash
git clone git@github.com:tangyuxia/VideoDyx3.git
```
2. 安装必须要python第三方库,如果命令是`pip3`就用`pip3`下载
```bash
pip install -r requirements.txt
```

---

## 注意
1. 本来代码中是想随机返回一个路线下载，考虑到部分路线可能会下载失败，所以返回的固定的第三，当路线少于三个的时候会报错
2. 合并完成后需要等一会才可以打开视频，刚合并完成就打开会报错，因为是用`python`异步操作的`ffmpeg`命令行工具，`python`命令执行完成了，但是`ffmpeg`命令行工具还在合并中
3. 配置文件中的主页地址可以修改，不过当这个电影路线少于三个的时候会报错
4. 需要科学上网才能抓数据
5. `pycharm`运行代码之前先把`m3u8`文件夹和`mp4`文件夹标记为已排除，就是标记为黄色的文件夹
6. 下载后的`ts`视频文件没有用代码删除

---