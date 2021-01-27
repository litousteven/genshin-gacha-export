import json
import requests
import urllib.parse
import sys
import copy

url = ""

FLAG_WRITE_CSV = 0
# 是否写入CSV
FLAG_WRITE_XLSX = 1
# 是否写入EXCEL
FLAG_SHOW_DETAIL = 0
# 是否展示详情
FLAG_CLEAN = 1
# 是否清除历史文件
FLAG_SHOW_REPORT = 1
# 是否显示抽卡统计报告


def main():

    print("检查URL", end="...", flush=True)
    checkApi(url)
    print("合法")

    print("获取物品信息", end="...", flush=True)
    gachaInfo = initGachaInfo()
    print("物品数：" + str(len(gachaInfo)))

    print("获取卡池信息", end="...", flush=True)
    gachaTypeIds, gachaTypeNames, gachaTypeDict = initGachaTypes()
    print(" ".join(gachaTypeNames))

    print("获取抽卡数据", end="...", flush=True)
    gachaLists = []
    for gachaTypeId in gachaTypeIds:
        if FLAG_SHOW_DETAIL:
            print(gachaTypeDict[gachaTypeId])
        gachaList = getGachaList(gachaInfo, gachaTypeId)
        gachaLists.append(gachaList)
        if not FLAG_SHOW_DETAIL:
            print(gachaTypeDict[gachaTypeId], end=" ", flush=True)
    print("")

    if FLAG_SHOW_REPORT:
        print("==========抽卡统计报告==========", flush=True)
        getGachaStatistics(gachaLists, gachaTypeNames)  ## 传入后reverse为时间升序（用于保底统计）

    if FLAG_CLEAN:
        print("清除历史文件", end="...", flush=True)
        import os

        del_paths = [name for name in os.listdir(sys.path[0]) if name.startswith("gacha") and (name.endswith(".csv") or name.endswith(".xlsx"))]
        for del_path in del_paths:
            try:
                os.remove(sys.path[0] + "\\" + del_path)
                print(del_path, end=" ", flush=True)
            except:
                pass
        print("")

    print("写入文件", end="...", flush=True)
    if FLAG_WRITE_CSV:
        writeCSV(gachaLists, gachaTypeIds)  ## 时间降序
        print("CSV", end=" ", flush=True)

    if FLAG_WRITE_XLSX:
        writeXLSX(gachaLists, gachaTypeNames)  ## 传入后reverse为时间升序（用于保底统计）
        print("XLSX", end=" ", flush=True)


def getGachaStatistics(gachaLists, gachaTypeNames):
    import pandas as pd
    import statistics
    gachaReportTemplate = """---------{}---------\n五星数量：{}\n五星百分比占比：{}\n平均出货：{}\n最欧的一次：{}\n最非的一次：{}"""
    collection_all = []
    totalGachaNum = 0
    for id in range(len(gachaLists)):
        gachaList = copy.deepcopy(gachaLists[id])
        totalGachaNum+=len(gachaList)
        gachaTypeName = gachaTypeNames[id]
        gachaList.reverse()
        splitList = [x.split(",") for x in gachaList]
        df = pd.DataFrame(splitList, columns=["time", "id", "name", "class", "star"])
        df["count"] = pd.Series(list(range(1, df.shape[0] + 1)))
        df["id"] = pd.to_numeric(df["id"])
        df["star"] = pd.to_numeric(df["star"])
        star5Count = df[df["star"] == 5].index.tolist()  ## 遇到五星时的总抽数
        df["gau5Count"] = df["count"]  ## 五星保底数
        i = 0
        gau5Count = []
        if len(star5Count) > 0:
            gau5Count.append(star5Count[0] + 1)  ## index start from 0

            for i in range(len(star5Count) - 1):
                df["gau5Count"] = df["gau5Count"].apply(lambda x: x - (star5Count[i] + 1) if (x > (star5Count[i] + 1) and x <= (star5Count[i + 1] + 1)) else x)
                gau5Count.append(star5Count[i + 1] - star5Count[i])

            df["gau5Count"] = df["gau5Count"].apply(lambda x: x - (star5Count[-1] + 1) if x > (star5Count[-1] + 1) else x)

        if len(gau5Count) > 0:
            out = gachaReportTemplate.format(gachaTypeName, len(gau5Count), str(round(len(gau5Count) / len(splitList) * 100, 4)) + "%", round(statistics.mean(gau5Count)), min(gau5Count), max(gau5Count))
        else:
            out = "---------{}---------\n尚未获得五星".format(gachaTypeName)

        ## 祈愿分类报告
        print(out, flush=True)
        # print("保底详情", df[df['star'] == 5])
        # print("保底数", gau5Count)
        # df.to_csv("{}.csv".format(id))

        collection_all += gau5Count

    report_all = gachaReportTemplate.format("合计", len(collection_all), str(round(len(collection_all) / totalGachaNum * 100, 4)) + "%", round(statistics.mean(collection_all)), min(collection_all), max(collection_all))

    ## 祈愿总计报告
    print(report_all, flush=True)
    print("==========统计报告结束==========")
    return


def getApi(gachaType, size, page):
    parsed = urllib.parse.urlparse(url)
    querys = urllib.parse.parse_qsl(parsed.query)
    param_dict = dict(querys)
    param_dict["size"] = size
    param_dict["gacha_type"] = gachaType
    param_dict["page"] = page
    param = urllib.parse.urlencode(param_dict)
    path = url.split("?")[0]
    api = path + "?" + param
    return api


def getInfo(item_id, gachaInfo):
    for info in gachaInfo:
        if info["item_id"] == item_id:
            return info["name"] + "," + info["item_type"] + "," + info["rank_type"]
    return "物品ID未找到"


def checkApi(url):
    if not url:
        print("未填入url")
        exit()
    if "getGachaLog" not in url:
        print("错误的url，检查是否包含getGachaLog")
        exit()
    try:
        requests.packages.urllib3.disable_warnings()
        r = requests.get(url, verify=False)
        s = r.content.decode("utf-8")
        j = json.loads(s)
    except Exception as e:
        print("API请求解析出错：" + str(e))
        exit()

    if not j["data"]:
        if j["message"] == "authkey valid error":
            print("authkey错误，请重新抓包获取url")
        else:
            print("数据为空，错误代码：" + j["message"])
        exit()
    return url


def getQueryVariable(variable):
    query = url.split("?")[1]
    vars = query.split("&")
    for v in vars:
        if v.split("=")[0] == variable:
            return v.split("=")[1]
    return ""


def initGachaInfo():
    requests.packages.urllib3.disable_warnings()
    region = getQueryVariable("region")
    lang = getQueryVariable("lang")
    gachaInfoUrl = "https://webstatic.mihoyo.com/hk4e/gacha_info/{}/items/{}.json".format(region, lang)
    r = requests.get(gachaInfoUrl, verify=False)
    s = r.content.decode("utf-8")
    gachaInfo = json.loads(s)
    return gachaInfo


def initGachaTypes():
    requests.packages.urllib3.disable_warnings()
    r = requests.get(url.replace("getGachaLog", "getConfigList"), verify=False)
    s = r.content.decode("utf-8")
    configList = json.loads(s)
    gachaTypeLists = []
    for gachaType in configList["data"]["gacha_type_list"]:
        gachaTypeLists.append([gachaType["key"], gachaType["name"]])
    gachaTypeLists.sort()
    gachaTypeDict = dict(gachaTypeLists)
    gachaTypeIds = []
    gachaTypeNames = []
    for gachaTypeId, gachaTypeName in gachaTypeLists:
        gachaTypeIds.append(gachaTypeId)
        gachaTypeNames.append(gachaTypeName)
    return gachaTypeIds, gachaTypeNames, gachaTypeDict


def getGachaList(gachaInfo, gachaTypeId):
    requests.packages.urllib3.disable_warnings()
    size = "20"
    # api限制一页最大20
    gachaList = []
    for page in range(1, 9999):
        api = getApi(gachaTypeId, size, page)
        r = requests.get(api, verify=False)
        s = r.content.decode("utf-8")
        j = json.loads(s)

        gacha = j["data"]["list"]
        if not len(gacha):
            break
        for i in gacha:
            time = i["time"]
            item_id = i["item_id"]
            info = time + "," + item_id + "," + getInfo(item_id, gachaInfo)
            gachaList.append(info)
            if FLAG_SHOW_DETAIL:
                print(info)
    return gachaList


def writeCSV(gachaLists, gachaTypes):
    for id in range(len(gachaTypes)):
        filename = f"{sys.path[0]}\\gacha{gachaTypes[id]}.csv"
        f = open(filename, "w", encoding="utf-8-sig")
        # 带BOM防止乱码
        for line in gachaLists[id]:
            f.write(line + "\n")
        f.close()


def writeXLSX(gachaLists, gachaTypeNames):
    import time

    import xlsxwriter

    t = time.strftime("%Y%m%d%H%M%S", time.localtime())
    workbook = xlsxwriter.Workbook(f"{sys.path[0]}\\gacha-{t}.xlsx")
    for id in range(0, len(gachaTypeNames)):
        gachaList = copy.deepcopy(gachaLists[id])
        gachaTypeName = gachaTypeNames[id]
        gachaList.reverse()
        header = "时间,编号,名称,类别,星级,总次数,保底内"
        worksheet = workbook.add_worksheet(gachaTypeName)
        content_css = workbook.add_format({"align": "left", "font_name": "微软雅黑", "border_color": "#c4c2bf", "border": 1})
        title_css = workbook.add_format({"align": "left", "font_name": "微软雅黑", "bg_color": "#ebebeb", "border_color": "#c4c2bf", "border": 1})
        excel_col = ["A", "B", "C", "D", "E", "F", "G"]
        excel_header = header.split(",")
        worksheet.set_column("A:A", 22)
        worksheet.set_column("C:C", 14)
        for i in range(len(excel_col)):
            # worksheet.write(f"{excel_col[i]}1", excel_header[i], border)
            worksheet.write(f"{excel_col[i]}1", excel_header[i], title_css)
        idx = 0
        pdx = 0
        for i in range(len(gachaList)):
            idx = idx + 1
            pdx = pdx + 1
            excel_data = gachaList[i].split(",")
            excel_data.extend([idx, pdx])
            excel_data[1] = int(excel_data[1])
            excel_data[4] = int(excel_data[4])
            for j in range(len(excel_col)):
                worksheet.write(f"{excel_col[j]}{i+2}", excel_data[j], content_css)
                # worksheet.write(f"{excel_col[j]}{i+2}", excel_data[j])
            if excel_data[4] == 5:
                pdx = 0

        star_5 = workbook.add_format({"bg_color": "#ebebeb", "color": "#bd6932", "bold": True})
        star_4 = workbook.add_format({"bg_color": "#ebebeb", "color": "#a256e1", "bold": True})
        star_3 = workbook.add_format({"bg_color": "#ebebeb"})
        # star_3 = workbook.add_format({"bg_color": "#ebebeb", "color": "#35aacc"})
        worksheet.conditional_format(f"A2:G{len(gachaList)+1}", {"type": "formula", "criteria": "=$E2=5", "format": star_5})
        worksheet.conditional_format(f"A2:G{len(gachaList)+1}", {"type": "formula", "criteria": "=$E2=4", "format": star_4})
        worksheet.conditional_format(f"A2:G{len(gachaList)+1}", {"type": "formula", "criteria": "=$E2=3", "format": star_3})

    workbook.close()


if __name__ == "__main__":
    main()
