# <coding:utf-8>
import json
import time

from main_switch import dict_switch
import os


def AlertLinux(sContent, sIMNumber):
    sUrl = "http://im.2980.com:8088/sendmsg?key=public_server_waring&accounts=%s&content=%s" % (sIMNumber, sContent)
    sShellCmd = "wget --quiet -O /dev/null '%s' &" % (sUrl)
    os.popen(sShellCmd)


def rrdtool_fetch(rrd_file, period, end_time, cf):
    str_command = '''rrdtool fetch --start="end - %s" --end="%s" -- %s %s''' % (period, end_time, rrd_file, cf)
    # print str_command
    str_rrd_content = os.popen(str_command)
    if not str_rrd_content:
        str_error = "rrdtool exec faild!command:%s" % (str_command)
        AlertLinux(str_error, 8766)
    return str_rrd_content


def filter_invalid(str_rrd_content):
    lst_rrd_content = str_rrd_content.readlines()
    lst_tmp = []
    # 过滤掉 -nan,trafice_in,trafic_out
    for str_line in lst_rrd_content:
        lst_line = str_line.split()
        if not lst_line:
            continue
        if "-nan" in lst_line:
            continue
        if 'traffic_in' in lst_line or 'traffic_out' in lst_line:
            continue
        lst_tmp.append(lst_line)
    return lst_tmp


def count_max_data(lst_rrd_content):
    max1 = 0.0
    max2 = 0.0
    for j in lst_rrd_content:
        data1 = float(j[1])
        data2 = float(j[2])
        if data1 > max1:  # 获得traffic_in和traffic_out30天内的最大值
            max1 = data1
        if data2 > max2:
            max2 = data2
    return max([round(max1 * 8 / 1000 / 1000, 2), round(max2 * 8 / 1000 / 1000, 2)])  # 将两个最大值进行比较，放回更大的


def count_ave_data(lst_rrd_content):
    sum1 = 0.0
    sum2 = 0.0
    count = 1
    for j in lst_rrd_content:
        data1 = float(j[1])
        data2 = float(j[2])
        sum1 = sum1 + data1
        sum2 = sum2 + data2
        count = count + 1
    return max([round(8 * sum1 / count / 1000 / 1000, 2), round(8 * sum2 / count / 1000 / 1000, 2)])  # 返回较大的值


# 重试次数必须限制。避免机房异常的情况下页面死掉！
def get_rrd_data(rrd_file, period, end_time, cf, iRetry=0):
    str_rrd_content = rrdtool_fetch(rrd_file, period, end_time, cf)
    # rrd可能正在写数据，此时读取数据将不完整。故而rrd会开启读锁，此时读取的数据将为空
    lst_rrd_content = filter_invalid(str_rrd_content)
    if cf == 'MAX':
        int_result = count_max_data(lst_rrd_content)
    elif cf == 'AVERAGE':
        int_result = count_ave_data(lst_rrd_content)
    if not int_result and iRetry > 2:
        iRetry -= 1
        sMsg = '读取到空数据，rrdfile:%s' % (rrd_file)
        AlertLinux(sMsg, 8766)
        time.sleep(1)
        # 递归的获得数据，非异步的情况下会引起界面加载慢的现象。
        int_result = get_rrd_data(rrd_file, period, end_time, cf, iRetry)
    return int_result


def get_all_rrd_data(period):
    cacti_rra_dir = '/var/lib/cacti/rra/'
    int_now_time = int(time.time())

    dict_result = {}
    for j in sorted(dict_switch):  # j表示机房
        # print j
        dict_result[j] = {}
        for i in dict_switch[j]:  # i表示线路
            # print i
            rrd_n = dict_switch[j][i][0]  # rrd文件的名字
            int_bound = dict_switch[j][i][2]  # 带宽的大小
            str_graph_dd = dict_switch[j][i][3]  # cacti中图表的id
            rrd_file_path = cacti_rra_dir + str(rrd_n)  # 拼接得到完整的名字
            max2 = get_rrd_data(rrd_file_path, period, int_now_time, 'MAX')  # 获得一个机房点
            dict_result[j][i] = {'used': max2, 'total': int_bound, 'graph_id': str_graph_dd}

    json_data = json.dumps(dict_result, sort_keys=True)  # 有sort_keys（对dict对象进行排序，我们知道默认dict是无序存放的）
    return json_data


if __name__ == '__main__':
    print get_all_rrd_data('5minute')
