#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 16-8-23 下午8:32
# @Author  : youzeshun
# 参考资料  :
# 说明     :
'''
# 在cacti中查询 rrd 和 rrd文件的对应关系：
select * from poller_item where rrd_path='/var/lib/cacti/rra/_traffic_in_5756.rrd';
'''
DICT_ADSL = {
    "10.10.10.121": {
        "eth0": {
            "purpose": "网站-运营",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_121_traffic_in_5571.rrd"
        }
    },
    "10.10.10.2": {
        "eth1": {
            "purpose": "电信",
            "equrrdment": "光纤出口",
            "max": 100,
            "rrd": "10_10_10_2_traffic_in_5690.rrd"
        }
    },
    "10.10.10.122.": {
        "eth0": {
            "purpose": "QQ",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_122_traffic_in_5573.rrd"
        }
    },
    "10.10.10.1": {
        "eth3": {
            "purpose": "睿江",
            "equrrdment": "光纤出口",
            "max": 100,
            "rrd": "10_10_10_1_traffic_in_5688.rrd"
        }
    },
    "10.10.10.126": {
        "eth0": {
            "purpose": "无线",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_126_traffic_in_5583.rrd"
        }
    },
    "10.10.10.123": {
        "eth0": {
            "purpose": "运营-公用机",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_123_traffic_in_5575.rrd"
        }
    },
    "10.10.10.125": {
        "eth0": {
            "purpose": "无线",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_125_traffic_in_5581.rrd"
        }
    },
    "10.10.10.127": {
        "eth0": {
            "purpose": "技术",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_127_traffic_in_5585.rrd"
        }
    },
    "10.10.10.120": {
        "eth0": {
            "purpose": "运营-行政",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_120_traffic_in_5569.rrd"
        }
    },
    "10.28.0.1": {
        "eth0": {
            "purpose": "成都电信2",
            "equrrdment": "光纤出口",
            "max": 20,
            "rrd": "_traffic_in_5756.rrd"
        },
        "eth3": {
            "purpose": "成都AD",
            "equrrdment": "光纤出口",
            "max": 20,
            "rrd": "_traffic_in_5758.rrd"
        }
    },
    "10.10.10.124": {
        "eth0": {
            "purpose": "策划",
            "equrrdment": "ADSL",
            "max": 200,
            "rrd": "adsl-10_10_10_124_traffic_in_5577.rrd"
        }
    }
}
