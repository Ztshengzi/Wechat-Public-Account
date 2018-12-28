#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 19:46 2017/11/7 

@author: acer
'''

# 保存获取到的车辆信息
traindic = {}
get_12306_count = 0
'''
查询两站之间的火车票信息

输入参数： <date> <from> <to>

12306 api:
'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2017-07-18&leftTicketDTO.from_station=NJH&leftTicketDTO.to_station=SZH&purpose_codes=ADULT'

'''
import requests
import json
import time

# 关闭https证书验证警告
requests.packages.urllib3.disable_warnings()

# 城市名代码查询字典
# key：城市名 value：城市代码
# from weixin.get12306.parse_station import get_parse_station
# station_dic=get_parse_station()
from weixin.get12306.stations import stations_dict as station_dic

# 反转k，v形成新的字典
code_dict = {v: k for k, v in station_dic.items()}


def get_query_url(text):
    # print(text)
    '''
    返回调用api的url链接
    '''
    # 解析参数 aggs[0]里是固定字符串：车票查询 用于匹配公众号接口
    args = str(text).split(' ')
    # print(args)
    try:
        date = args[0]
        from_station_name = args[1]
        to_station_name = args[2]
        from_station = station_dic[from_station_name]
        to_station = station_dic[to_station_name]
    except:
        date, from_station, to_station = '--', '--', '--'
        # 将城市名转换为城市代码

    # api url 构造
    """
    https://kyfw.12306.cn/otn/leftTicket/query?
    leftTicketDTO.train_date=2017-12-01&leftTicketDTO.from_station=BJP&
    leftTicketDTO.to_station=SHH&purpose_codes=ADULT
    """
    """
    https://kyfw.12306.cn/otn/leftTicket/queryO?
    leftTicketDTO.train_date=2018-04-10&
    leftTicketDTO.from_station=SHH&
    leftTicketDTO.to_station=BJP&purpose_codes=ADULT
    """
    """
    https://kyfw.12306.cn/otn/leftTicket/queryO?
    leftTicketDTO.train_date=2018-04-10&
    leftTicketDTO.from_station=SHH&
    leftTicketDTO.to_station=BJP&
    purpose_codes=ADULT
    """
    url = (
        'https://kyfw.12306.cn/otn/leftTicket/query?'
        'leftTicketDTO.train_date={}&'
        'leftTicketDTO.from_station={}&'
        'leftTicketDTO.to_station={}&'
        'purpose_codes=ADULT'
    ).format(date, from_station, to_station)
    print(url)
    return url


"""
def query_train_info(url):
    '''
    查询火车票信息：
    返回 信息查询列表
    '''

    info_list = []
    try:
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        #r = requests.get(url,verify=False,headers=headers)
        r = requests.get(url)
        # 获取返回的json数据里的data字段的result结果
        raw_trains = r.json()['data']['result']
        for raw_train in raw_trains:
            # 循环遍历每辆列车的信息
            data_list = raw_train.split('|')

            # 车次号码
            train_no = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = code_dict[from_station_code]
            # 终点站
            to_station_code = data_list[7]
            to_station_name = code_dict[to_station_code]
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 一等座
            first_class_seat = data_list[31] or '--'
            # 二等座
            second_class_seat = data_list[30] or '--'
            # 软卧
            soft_sleep = data_list[23] or '--'
            # 硬卧
            hard_sleep = data_list[28] or '--'
            # 硬座
            hard_seat = data_list[29] or '--'
            # 无座
            no_seat = data_list[26] or '--'

            # 打印查询结果
            info = (
            '车次:{}\n出发站:{}\n目的地:{}\n出发时间:{}\n到达时间:{}\n消耗时间:{}\n座位情况：\n 一等座：「{}」 \n二等座：「{}」\n软卧：「{}」\n硬卧：「{}」\n硬座：「{}」\n无座：「{}」\n\n'.format(
                train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,
                second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))
            info_list.append(info)
        return info_list
    except:
        return str
"""


def GetInfoTrain(url, flag=False):
    """
     :param url:请求12306车次信息链接 
     :param flag: 微信端与网页端请求标志位
     :return: 返回字典：{'train_info_list':train_info_list,'info':info,'status':1}
                train_info_list  车次信息列表，info 返回提示信息  status 返回请求状态码
    """

    global get_12306_count
    if 'from_station=--' in url:
        get_12306_count = 0
        return {'train_info_list': [], 'info': '出发地/目的地站点名错误，请输入正确站点名！', 'status': 0}
    train_info_list = []
    try:
        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        # r = requests.get(url,verify=False,headers=headers)
        r = requests.get(url)
        # 获取返回的json数据里的data字段的result结果
        raw_trains = r.json()['data']['result']
        # print(raw_trains)
        for raw_train in raw_trains:

            # 循环遍历每辆列车的信息
            data_list = raw_train.split('|')
            train_no = data_list[3]
            # 出发站
            from_station_code = data_list[6]
            from_station_name = code_dict[from_station_code]
            # 终点站
            to_station_code = data_list[7]
            to_station_name = code_dict[to_station_code]
            # 出发时间
            start_time = data_list[8]
            # 到达时间
            arrive_time = data_list[9]
            # 总耗时
            time_fucked_up = data_list[10]
            # 商务座
            business_seat = data_list[32] or '--'
            # 高级动卧
            Advanced_dynamic_supine = data_list[21] or '--'
            # 动卧
            Pneumatic_horizontal = data_list[33] or '--'
            # 一等座
            first_class_seat = data_list[31] or '--'
            # 二等座
            second_class_seat = data_list[30] or '--'
            # 软卧
            soft_sleep = data_list[23] or '--'
            # 硬卧
            hard_sleep = data_list[28] or '--'
            # 硬座
            hard_seat = data_list[29] or '--'
            # 无座
            no_seat = data_list[26] or '--'
            if flag:
                info_dic = {'train_no': train_no,
                            'from_station_name': from_station_name,
                            'to_station_name': to_station_name,
                            'start_time': start_time,
                            'arrive_time': arrive_time,
                            'time_fucked_up': time_fucked_up,
                            'first_class_seat': first_class_seat,
                            'second_class_seat': second_class_seat,
                            'soft_sleep': soft_sleep,
                            'hard_sleep': hard_sleep,
                            'hard_seat': hard_seat,
                            'no_seat': no_seat,
                            'Pneumatic_horizontal': Pneumatic_horizontal,
                            'Advanced_dynamic_supine': Advanced_dynamic_supine,
                            'business_seat': business_seat
                            }
                train_info_list.append(info_dic)
            else:
                info = (
                    '车次:{}\n出发站:{}\n目的地:{}\n出发时间:{}\n到达时间:{}\n消耗时间:{}\n座位情况：\n 一等座：「{}」 \n二等座：「{}」\n软卧：「{}」\n硬卧：「{}」\n硬座：「{}」\n无座：「{}」\n动卧：「{}」\n高级动卧：「{}」\n商务：「{}」\n'.format(
                        train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up,
                        first_class_seat,second_class_seat, soft_sleep,
                        hard_sleep, hard_seat,no_seat,Pneumatic_horizontal,Advanced_dynamic_supine,
                        business_seat,))
                train_info_list.append(info)
        info = "查询到" + str(len(train_info_list)) + "班次:"
        get_12306_count = 0
        return {'train_info_list': train_info_list, 'info': info, 'status': 1}
    except Exception as e:
        get_12306_count = get_12306_count + 1
        print(get_12306_count)
        if get_12306_count > 10:
            get_12306_count = 0
            return {'train_info_list': [], 'info': '服务器繁忙，请稍后再试!', 'status': 0}
        return GetInfoTrain(url, flag)
