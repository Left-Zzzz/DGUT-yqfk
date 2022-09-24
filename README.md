2022-9-24
验证中心接口更改，对密码进行了动态加密，遂本次脚本改用模拟点击进行通过验证中心验证。
改用了seleniumwire进行模拟点击鉴权。需要下载google-chrome和chromedirver（我这里都是v105的），pip需要下载selenium和seleniumwire。

这里以ubuntu为例
## ubuntu
### 下载google chrome
```bash
# 对于谷歌Chrome32位版本，使用如下链接
wget https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb

# 对于64位版本可以使用如下链接下载
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb 

# 下载完后，运行如下命令安装
sudo dpkg -i google-chrome*; sudo apt-get -f install 
```

### 下载chrome driver
```bash
# 看一眼google chrome版本号
google-chrome --version
=> Google Chrome 105.0.5195.125

# 版本是v105的，去https://chromedriver.storage.googleapis.com/index.html上找对应适配的chromedriver
# 一般来说，v70版本以后的googlechrome和chromedriver的大的版本号是对应的
# 这里直接下载版本号为105.0.5195.52的chromedriver
wget https://chromedriver.storage.googleapis.com/105.0.5195.52/chromedriver_linux64.zip

# 直接解压到脚本运行目录
unzip chromedriver_linux64.zip
```

### pip安装selenium和selenium-wire
```bash
pip install selenium
pip install selenium-wire
```


------
2021.12.23
新版疫情防控自动打卡脚本，将旧版相关api更改成了新版api，脚本恢复正常使用。
------

## Usage

```
USERNAME   # 学号
PASSWORD   # 中央认证系统密码
SCKEY      # 消息推送UID
```

消息推送获取UID
关注公众号：wxpusher，然后点击「我的」-「我的UID」查询到UID。

默认在 00:20, 01:20, 09:00 的时候提交

### 方法一 (docker-compose)

```yaml
version: "3.1"

services:
  yqfk:
    image: masterkenway/dgut_yqfk
    environment:
      - USERNAME=
      - PASSWORD=
      - SCKEY=
    restart: always
```

### 方法二 (screen)

可以使用`screen`将程序放置在后台运行

```shell script
$ git clone https://github.com/MasterKenway/DGUT-yqfk.git && cd DGUT-yqfk 
$ pip install -r requirements.txt # 如果运行时报错找不到模块，请确认安装了pip3并将本条命令开头的pip改为pip3
$ screen -US yqfk # Ctrl + A + D 离开 screen
$ python3 yqfk.py USERNAME PASSWORD SCKEY
```

