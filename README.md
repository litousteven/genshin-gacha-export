# 原神抽卡记录导出

NGA原帖：https://bbs.nga.cn/read.php?&tid=25004616  

抽卡记录分析工具 from [@笑沐泽](https://bbs.nga.cn/read.php?tid=25004616&page=16#pid491033187Anchor)  
https://voderl.github.io/genshin-gacha-analyzer/

[[闲聊杂谈] 抽卡记录导出两键导出工具](https://bbs.nga.cn/read.php?tid=25559039) from [@lvlvl](https://bbs.nga.cn/nuke.php?func=ucp&uid=2260231)  
https://github.com/biuuu/genshin-gacha-export

抽卡记录导出工具js版 https://github.com/sunfkny/genshin-gacha-export-js  

Tip: 1.3版本更新后api只能获取6个月历史记录

## 功能

 - 读取客户端日志文件中的url
 - 记录历史url，如果可用无需重新抓包
 - 自动抓包本机api请求
 - 导出抽卡记录为带格式的excel表格
 - 展示抽卡报告 [抽卡报告预览](抽卡报告.md)
 - 清除历史生成的excel表格
 - 可选手动输入url
 - exe版无需fiddler和python环境


## 使用方法
解压并运行 genshin-gacha-export.exe  
- 读取日志文件模式：
    - 只需要最近打开过抽卡记录页面直接运行即可，无需运行游戏
- 抓包模式：  
    - **运行之前务必先关闭第三方代理、加速器否则会抓不到**
    - 打开游戏-祈愿-历史记录  
    - 等待程序获取数据生成表格和抽卡报告  

## 配置文件 config.json

```
{
    "FLAG_CLEAN":false,
    "FLAG_MANUAL_INPUT_URL":false,
    "FLAG_SHOW_REPORT":true,
    "FLAG_USE_LOG_URL":true,
    "FLAG_USE_CONFIG_URL":true,
    "FLAG_WRITE_XLSX":true,
    "FLAG_USE_CAPTURE":true,
    "url":""
}
```
| 配置名称              | 含义                   | 类型 | 默认值 |
| --------------------- | ---------------------- | ---- | ------ |
| FLAG_CLEAN            | 清除历史生成的excel表格 | bool | false   |
| FLAG_MANUAL_INPUT_URL | 手动输入url            | bool | false  |
| FLAG_SHOW_REPORT      | 展示抽卡报告           | bool | true   |
| FLAG_WRITE_XLSX       | 生成抽卡记录excel表格 | bool |  true  |
| FLAG_USE_LOG_URL       | 使用原神客户端日志中的url | bool |  true  |
| FLAG_USE_CONFIG_URL       | 使用配置文件缓存的历史url | bool |  true  |
| FLAG_USE_CAPTURE       | 抓包功能 | bool |  true  |
| url                   | 包含getGachaLog的url  | str  |        |


## 更新日志

https://github.com/sunfkny/genshin-gacha-export/wiki/%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97
