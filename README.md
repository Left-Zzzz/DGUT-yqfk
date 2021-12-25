
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

