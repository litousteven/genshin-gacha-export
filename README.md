# 原神抽卡记录导出

NGA原帖：https://bbs.nga.cn/read.php?&tid=25004616

视频教程：https://www.bilibili.com/video/BV1qA411W7Lo/

## 具体操作：

- 用fiddler抓包获取类似`https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog?xxxxxx`的链接（右键-复制-仅复制网址）

- 将链接填入`url`变量并运行

- 用excle打开`gechaxxx.csv`表格，第一列其实是精确到秒的，有需要可以设置一下格式，对excel精通的可以像我一样做一个条件格式，还可以做数据查询，打开自动刷新等等

## 卡池和物品数据

getConfigList.json是卡池数据，来自`https://hk4e-api.mihoyo.com/event/gacha_info/api/getConfigList?xxxxxxx`，如果有新卡池就下载替换这个json

gacha_info.json是物品数据，来自`https://webstatic.mihoyo.com/hk4e/gacha_info/cn_gf01/items/zh-cn.json`，如果有新物品就下载替换这个json
