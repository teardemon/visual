# 通用可视化接口演示
打开页面一：

http://192.168.165.200:82/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10}}}


打开页面二：
http://192.168.165.200:82/custom/output/?chart=bar&key=adsl&timeout=5


在页面一中修改参数data中的purpose.更改后的url如：
http://192.168.165.200:82/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "行政","down_total": 200,"up_total": 35,"down_used": 10,"up_used": 20}}}


然后刷新页面一，此时看页面二(无需手动刷新)，页面二也变化了

## 参数/格式说明：
数据输入链接：　http://ip:port/custom/input/
	参数:
	live 　　是否在当前页面直接显示效果　可选　默认0
	chart : 选用哪种图形显示数据，当live为１时才有效
	key 　　　访问数据的key 必选
	data 　　数据
	
数据输出链接：　http://ip:port/custom/out/
	参数：
	key : 图像化对应key的数据
	chart : 选用哪种图形显示数据，目前是代码为demo,仅有默认的bar
	timeout: 更新数据的频率

# 更为完整的demo
http://192.168.165.200:82/custom/input/?live=1&chart=bar&key=adsl&data={"10.10.10.121": {"eth0": {"purpose": "网站-运营","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_121_traffic_in_5571.rrd"}},"10.10.10.2": {"eth1": {"purpose": "电信","equrrdment": "光纤出口","down_total": 100,"up_total": 100,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "10_10_10_2_traffic_in_5690.rrd"}},"10.10.10.122.": {"eth0": {"purpose": "QQ","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_122_traffic_in_5573.rrd"}},"10.10.10.1": {"eth3": {"purpose": "睿江","equrrdment": "光纤出口","down_total": 100,"up_total": 100,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "10_10_10_1_traffic_in_5688.rrd"}},"10.10.10.126": {"eth0": {"purpose": "无线1","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_126_traffic_in_5583.rrd"}},"10.10.10.123": {"eth0": {"purpose": "运营-公用机","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_123_traffic_in_5575.rrd"}},"10.10.10.125": {"eth0": {"purpose": "无线2","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_125_traffic_in_5581.rrd"}},"10.10.10.127": {"eth0": {"purpose": "技术","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_127_traffic_in_5585.rrd"}},"10.10.10.120": {"eth0": {"purpose": "运营-行政","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"rrd": "adsl-10_10_10_120_traffic_in_5569.rrd"}},"10.28.0.1": {"eth0": {"purpose": "成都电信2","equrrdment": "光纤出口","down_total": 20,"up_total": 20,"down_used": 10,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "_traffic_in_5756.rrd"},"eth3": {"purpose": "成都AD","equrrdment": "光纤出口","down_total": 100,"up_total": 20,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "_traffic_in_5758.rrd"}},"10.10.10.124": {"eth0": {"purpose": "策划","equrrdment": "ADSL","down_total": 200,"up_total": 35,"down_used": 100,"up_used": 10,"zabbix_graph_id": 'yzs-1',"rrd": "adsl-10_10_10_124_traffic_in_5577.rrd"}}}

