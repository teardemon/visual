# 部署

```
git clone git@youzeshun.com:zeshun/visual.git
sudo python visual/manage.py runserver 0.0.0.0:82
```


# 维护
## 增减idc节点
1.运行　clear_cache.sh　清除缓存
2.将节点剔除/加入排序列表　idcconfig.py的LIST_LINK_SORT

## 页面信息不准确
### 图像上没有数据
可能是割接引起的交换机网口改变，需要更新线路流量和网口的映射关系。
清空缓存dash clear_cache.sh
代码会自动生成新缓存

## 报警说明
### 提示信息
1. IP: 10.32.17.183 116.211.137.1通过接口查询关键字"Traffic on interface eth0"没能在zabbix接口中获得关于zabbix流量图的url信息
是新增的交换机ip,但是在网口和ip的映射中不存在。所以被判断为服务器了。而服务器中，流量是通过包含信息"Traffic on interface eth0"的键取得的。


# 通用可视化接口演示
使用接口：
打开页面一输入下面的链接，将data传入
http://192.168.165.200:82/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10}}}


效果：打开页面二
http://192.168.165.200:82/custom/output/?chart=bar&key=adsl&timeout=5


当更改传入data后，页面二的图形会变化(无需手动刷新)（更改后的url如：）
http://192.168.165.200:82/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "行政","down_total": 200,"up_total": 35,"down_used": 10,"up_used": 20}}}


## 参数/格式说明：
数据输入链接：　http://ip:port/custom/input/
	参数:
	live 　　是否在当前页面直接显示效果　可选　默认0
	chart : 选用哪种图形显示数据，当live为１时才有效
	key 　　　访问数据的key 必选
	data 　　数据
	date   时间，默认是后端接收到数据的时间
	
数据输出链接：　http://ip:port/custom/out/
	参数：
	key : 图像化对应key的数据
	chart : 选用哪种图形显示数据，目前是代码为demo,仅有默认的bar
	timeout: 更新数据的频率
# 传入的数据格式data说明
## 必须的参数：
{
    "10.32.64.134": {
        "eth0": {
            "purpose": "用于代码部署", 
            "down_total": 200, 
            "up_total": 35, 
            "down_used": 100, 
            "up_used": 10
        }
    }
}

## 完整版本格式说明
{
    "10.32.64.134": {
        "eth0": {
            "purpose": "用于代码部署", //用途，如：ＱＱ，部门
            "equrrdment": "虚拟机", //设备，如光纤,adsl
            "down_total": 200, //下载总带宽，单位m/s
            "up_total": 35, //上行总带宽,单位m/s
            "down_used": 100, //上行已用,单位m/s
            "up_used": 10, //下行已用，单位m/s
            "zabbix_graph_id": "yzs-1"　//该ｉｐ的网口eth0对应的zabbix_graph_id
        }
    }
}


## 传入时间
http://127.0.0.1/custom/input/?live=1&date=我是时间&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10}}}

# 更为完整的demo
http://192.168.165.200:82/custom/input/?live=1&chart=bar&key=adsl&data={ "10.10.10.121": { "eth0": { "purpose": "网站-运营", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.2": { "eth1": { "purpose": "电信", "equrrdment": "光纤出口", "down_total": 100, "up_total": 100, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.122.": { "eth0": { "purpose": "QQ", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.1": { "eth3": { "purpose": "睿江", "equrrdment": "光纤出口", "down_total": 100, "up_total": 100, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.126": { "eth0": { "purpose": "无线1", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.123": { "eth0": { "purpose": "运营-公用机", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.125": { "eth0": { "purpose": "无线2", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.127": { "eth0": { "purpose": "技术", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.120": { "eth0": { "purpose": "运营-行政", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10 } }, "10.28.0.1": { "eth0": { "purpose": "成都电信2", "equrrdment": "光纤出口", "down_total": 20, "up_total": 20, "down_used": 10, "up_used": 10, "zabbix_graph_id": "yzs-1" }, "eth3": { "purpose": "成都AD", "equrrdment": "光纤出口", "down_total": 100, "up_total": 20, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } }, "10.10.10.124": { "eth0": { "purpose": "策划", "equrrdment": "ADSL", "down_total": 200, "up_total": 35, "down_used": 100, "up_used": 10, "zabbix_graph_id": "yzs-1" } } }

# 更新上传最大/下载最大的接口
http://127.0.0.1/adsl/input?data={%2210.10.10.121%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E7%BD%91%E7%AB%99-%E8%BF%90%E8%90%A5%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.2%22:%20{%22eth1%22:%20{%22purpose%22:%20%22%E7%94%B5%E4%BF%A1%22,%22equrrdment%22:%20%22%E5%85%89%E7%BA%A4%E5%87%BA%E5%8F%A3%22,%22down_total%22:%20100,%22up_total%22:%20100,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.122.%22:%20{%22eth0%22:%20{%22purpose%22:%20%22QQ%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.1%22:%20{%22eth3%22:%20{%22purpose%22:%20%22%E7%9D%BF%E6%B1%9F%22,%22equrrdment%22:%20%22%E5%85%89%E7%BA%A4%E5%87%BA%E5%8F%A3%22,%22down_total%22:%20100,%22up_total%22:%20100,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.126%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E6%97%A0%E7%BA%BF1%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.123%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E8%BF%90%E8%90%A5-%E5%85%AC%E7%94%A8%E6%9C%BA%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.125%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E6%97%A0%E7%BA%BF2%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.127%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E6%8A%80%E6%9C%AF%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.120%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E8%BF%90%E8%90%A5-%E8%A1%8C%E6%94%BF%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010}},%2210.28.0.1%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E6%88%90%E9%83%BD%E7%94%B5%E4%BF%A12%22,%22equrrdment%22:%20%22%E5%85%89%E7%BA%A4%E5%87%BA%E5%8F%A3%22,%22down_total%22:%2020,%22up_total%22:%2020,%22down_used%22:%2010,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22},%22eth3%22:%20{%22purpose%22:%20%22%E6%88%90%E9%83%BDAD%22,%22equrrdment%22:%20%22%E5%85%89%E7%BA%A4%E5%87%BA%E5%8F%A3%22,%22down_total%22:%20100,%22up_total%22:%2020,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}},%2210.10.10.124%22:%20{%22eth0%22:%20{%22purpose%22:%20%22%E7%AD%96%E5%88%92%22,%22equrrdment%22:%20%22ADSL%22,%22down_total%22:%20200,%22up_total%22:%2050,%22down_used%22:%20100,%22up_used%22:%2010,%22zabbix_graph_id%22:%20%22yzs-1%22}}}


