# -*- coding:UTF-8 -*-

import json
import os
import requests
import sqlite3
import threading
import downloader
from entity.Product import Product

from xlrd import open_workbook
from xlwt import *
# from xlutils.copy import copy

base_url = "http://pc.findeng.com/mobile/api/v2/product/"

payload = ""
headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Connection': "keep-alive",
    'Cookie': "SESSION=73e6dff2-8408-4411-a0ec-d2aa3efd39d6",
    'Host': "pc.findeng.com",
    'Referer': "http://pc.findeng.com/detailed.html?detailed_id=32829",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    'cache-control': "no-cache",
    'Postman-Token': "e77d50a4-c7dc-4ab8-ae52-cf7d7e5f6e9f",
    'X-Requested-With': "XMLHttpRequest"
    }


# def dict2product(product):
#     return Product(str(product['productId']), product['productName'], product['productAliasName'],
#                    product['productBrand'],
#                    product['productCover'], product['productPngPic'], product['descriptionPic'], product['keyWord'],
#                    product['productType'],
#                    product['productCode'], product['productStyle'], product['productMaterial'], product['productSpace'],
#                    product['importantParam'])


# 下载产品信息
def download_product_info(product):
    # 产品id
    product_id = str(product['productId'])
    product_name = product['productName']
    # 创建产品目录
    # product_dir = 'product' + os.sep + product_id + '_' + product_name + os.sep
    product_dir = 'product' + os.sep + product_id + os.sep
    # 如果产品目录不存在，则创建目录
    if not os.path.exists(product_dir):
        os.makedirs(product_dir)

    # 将产品信息保存到文本文件
    save_product_to_text(product_dir, product)
    # 下载相关图片
    download_product_images(product_dir, product)


# 将产品信息保存到文本文件
def save_product_to_text(product_dir, product):
    try:
        product_id = str(product['productId'])
        f = open(product_dir + product_id + '_product_data.txt', 'wb')
        f.write(str(product).encode("utf-8"))
        f.close
    except Exception as e:
        print(e)


# 下载产品相关文件
def download_product_images(product_dir, product):
    # 下载相关图片

    # 产品配灯图
    try:
        product_png_pic = product['productPngPic']
        downloader.download_image_with_prefix(product_dir, str(product['productId']) + '_diy_', product_png_pic)
    except Exception as e:
        pass

    # 产品封面
    try:
        product_cover = product['productCover']
        product_cover_dir = product_dir + os.sep + 'cover' + os.sep
        # 如果产品目录不存在，则创建目录
        if not os.path.exists(product_cover_dir):
            os.makedirs(product_cover_dir)
        downloader.download_image_with_prefix(product_cover_dir, '', product_cover)
    except Exception as e:
        pass

    # 产品详情图片
    product_detail_dir = product_dir + os.sep + 'detail' + os.sep
    # 如果产品目录不存在，则创建目录
    if not os.path.exists(product_detail_dir):
        os.makedirs(product_detail_dir)
    for i in range(17):
        pic_no = str(i + 1)

        try:
            des_pic_url = product['descriptionPic' + pic_no]
        except Exception as e:
            break

        if len(des_pic_url) > 0:
            downloader.download_image_with_prefix(product_detail_dir, str(product['productId']) + '_' + pic_no + '_', des_pic_url)


# TODO 将产品信息保存到xls文件




def ready_download_product(min, max):

    for product_id in range(min, max):
        print('开始下载：', product_id)

        product_detail_url = base_url + str(product_id)

        response = requests.request("GET", product_detail_url, data=payload, headers=headers)
        response_json = response.json()
        json_code = response_json['code']
        json_msg = response_json['msg']
        json_arr = response_json['arr']

        if 2000 == json_code or 0 == json_code:
            if len(json_arr) > 0:
                for item in json_arr:
                    # 产品信息
                    download_product_info(item)
                continue

        print('获取数据失败：', product_id, 'json_code', json_code, 'json_msg', json_msg)







if __name__ == "__main__":

    # TODO 通过多线程获取数据，分10个线程

    total_product = 40000
    thread_per_number = 5000

    for i in range( int(total_product / thread_per_number) ):
        min = i * thread_per_number
        max = (i+1) * thread_per_number
        t = threading.Thread(target=ready_download_product, args=(min, max,))
        t.start()




    # for product_id in range(1, 40000):
    #     print('开始下载：', product_id)
    #
    #     product_detail_url = base_url + str(product_id)
    #
    #     response = requests.request("GET", product_detail_url, data=payload, headers=headers)
    #     response_json = response.json()
    #     json_code = response_json['code']
    #     json_msg = response_json['msg']
    #     json_arr = response_json['arr']
    #
    #     if 2000 == json_code or 0 == json_code:
    #         if len(json_arr) > 0:
    #             for item in json_arr:
    #                 # 产品信息
    #                 download_product_info(item)
    #             continue
    #
    #     print('获取数据失败：', product_id, 'json_code', json_code, 'json_msg', json_msg)




#
# productId 产品id
# productName 产品名称
# productAliasName 产品别名
# productBrand 品牌
# productCover 封面图
# productPngPic 配灯图
# descriptionPic 产品详情图
# keyWord 关键词
# productType 产品分类
# productCode 产品代号
# productStyle 风格
# productMaterial 材质
# productSpace 空间
# importantParam 其它参数


