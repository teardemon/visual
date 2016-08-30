# visual 需要达到的目的
我这尝试提供可视化的服务接口，数据传入接口后，能在当前页面直接可视化，其他已打开了指定url的页面刷新后也能有同样的效果
之后有新的可视化需求出现，我这会按照这套标志提供接口，而不是单独为新需求写后端逻辑。

这里有个demo，大家可是试下效果。

1.在浏览器复制粘贴这个url：
http://127.0.0.1/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10}}}

2.任意修改url后刷新，可视化的内容也会改变

3.新打开一个页面:
http://127.0.0.1/zabbix/output/?key=adsl

格式说明：
live == 1 进行live
key : 访问数据的key，用于其他页面访问被可视化数据
data : 被可视化的主体数据
chart : 选用哪种图形显示数据，目前是代码为demo,仅有默认的bar可选


# 可视化live
live == 1 进行live
key : 访问数据的key
data : 数据

## 演示如下:
http://127.0.0.1/zabbix/input/?live=1&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10}}}


# 指定使用哪种图形进行可视化显示
chart : 使用那种图形进行可视化，目前仅bar可用。默认也是bar

## 演示如下:
http://127.0.0.1/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10}}}

格式说明:
timeout : 刷新的间隔
http://127.0.0.1/custom/output/?key=adsl&chart=bar&timeout=10

# 更为完整的demo
http://127.0.0.1/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_121_traffic_in_5571.rrd"}},"10.10.10.2": {"eth1": {"purpose": "电信","equrrdment": "光纤出口","down_total": 100,"up_total": 100,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "10_10_10_2_traffic_in_5690.rrd"}},"10.10.10.122.": {"eth0": {"purpose": "QQ","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_122_traffic_in_5573.rrd"}},"10.10.10.1": {"eth3": {"purpose": "睿江","equrrdment": "光纤出口","down_total": 100,"up_total": 100,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "10_10_10_1_traffic_in_5688.rrd"}},"10.10.10.126": {"eth0": {"purpose": "无线1","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_126_traffic_in_5583.rrd"}},"10.10.10.123": {"eth0": {"purpose": "运营-公用机","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_123_traffic_in_5575.rrd"}},"10.10.10.125": {"eth0": {"purpose": "无线2","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_125_traffic_in_5581.rrd"}},"10.10.10.127": {"eth0": {"purpose": "技术","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_127_traffic_in_5585.rrd"}},"10.10.10.120": {"eth0": {"purpose": "运营-行政","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"rrd": "adsl-10_10_10_120_traffic_in_5569.rrd"}},"10.28.0.1": {"eth0": {"purpose": "成都电信2","equrrdment": "光纤出口","down_total": 20,"up_total": 20,"down_used": 10,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "_traffic_in_5756.rrd"},"eth3": {"purpose": "成都AD","equrrdment": "光纤出口","down_total": 100,"up_total": 20,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "_traffic_in_5758.rrd"}},"10.10.10.124": {"eth0": {"purpose": "策划","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_124_traffic_in_5577.rrd"}}}
