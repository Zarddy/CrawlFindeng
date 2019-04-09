# -*- coding:UTF-8 -*-

import os
import requests
import threading
import xlwt
import downloader

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

excel_titles = ['productId（产品id）', 'productName（产品名称）', 'productAliasName（产品别名）', 'productBrand（品牌）',
                'keyWord（关键词）', 'productType（产品分类）', 'productCode（产品编号）',
                'productStyle（风格）', 'productMaterial（材质）', 'productSpace（空间）', 'importantParam（其它参数）',
                'productCover（封面图）', 'productPngPic（配灯图）',
                'descriptionPic1（产品详情图）', 'descriptionPic2', 'descriptionPic3',
                'descriptionPic4', 'descriptionPic5', 'descriptionPic6',
                'descriptionPic7', 'descriptionPic8', 'descriptionPic9',
                'descriptionPic10', 'descriptionPic11', 'descriptionPic12',
                'descriptionPic13', 'descriptionPic14', 'descriptionPic15',
                'descriptionPic16']

# def dict2product(product):
#     return Product(str(product['productId']), product['productName'], product['productAliasName'],
#                    product['productBrand'],
#                    product['productCover'], product['productPngPic'], product['descriptionPic'], product['keyWord'],
#                    product['productType'],
#                    product['productCode'], product['productStyle'], product['productMaterial'], product['productSpace'],
#                    product['importantParam'])


def ready_download_product(start_index, end_index):

    for product_id in range(start_index, end_index):
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


# 下载产品信息
def download_product_info(product):

    # 产品id
    product_id = str(product['productId'])

    # 获取产品配灯图，如果没有配灯图，则不下载
    try:
        product_png_pic = product['productPngPic']
        if len(product_png_pic) == 0:
            print("没有配灯图的产品id：", product_id)
            return
    except Exception as e:
        print("没有配灯图的产品id：", product_id)
        return

    # 创建产品目录
    product_dir = 'findeng_com_product' + os.sep + product_id + os.sep
    # 如果产品目录不存在，则创建目录
    if not os.path.exists(product_dir):
        os.makedirs(product_dir)
    else:
        # 如果该文件夹已存在，表示已经下载过产品信息
        return

    # 将产品信息保存到文本文件
    save_product_to_text(product_dir, product)
    # 将产品信息保存到excel文件
    save_product_info_to_xls(product_dir, product)
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


# 将产品信息保存到xls文件
def save_product_info_to_xls(product_dir, product):
    # TODO 把数据保存到excel文件中
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('product info')

    # 创建表头
    for i in range(len(excel_titles)):
        title = excel_titles[i]
        sheet.write(0, i, title) # 在第0行第1列写入内容

    try:
        productId = product['productId']
    except Exception as e:
        productId = ''

    try:
        productName = product['productName']
    except Exception as e:
        productName = ''

    try:
        productAliasName = product['productAliasName']
    except Exception as e:
        productAliasName = ''

    try:
        productBrand = product['productBrand']
    except Exception as e:
        productBrand = ''

    try:
        keyWord = product['keyWord']
    except Exception as e:
        keyWord = ''

    try:
        productType = product['productType']
    except Exception as e:
        productType = ''

    try:
        productCode = product['productCode']
    except Exception as e:
        productCode = ''

    try:
        productStyle = product['productStyle']
    except Exception as e:
        productStyle = ''

    try:
        productMaterial = product['productMaterial']
    except Exception as e:
        productMaterial = ''

    try:
        productSpace = product['productSpace']
    except Exception as e:
        productSpace = ''

    try:
        importantParam = product['importantParam']
    except Exception as e:
        importantParam = ''

    try:
        productCover = product['productCover']
    except Exception as e:
        productCover = ''

    try:
        productPngPic = product['productPngPic']
    except Exception as e:
        productPngPic = ''

    try:
        descriptionPic1 = product['descriptionPic1']
    except Exception as e:
        descriptionPic1 = ''

    try:
        descriptionPic2 = product['descriptionPic2']
    except Exception as e:
        descriptionPic2 = ''

    try:
        descriptionPic3 = product['descriptionPic3']
    except Exception as e:
        descriptionPic3 = ''

    try:
        descriptionPic4 = product['descriptionPic4']
    except Exception as e:
        descriptionPic4 = ''

    try:
        descriptionPic5 = product['descriptionPic5']
    except Exception as e:
        descriptionPic5 = ''

    try:
        descriptionPic6 = product['descriptionPic6']
    except Exception as e:
        descriptionPic6 = ''

    try:
        descriptionPic7 = product['descriptionPic7']
    except Exception as e:
        descriptionPic7 = ''

    try:
        descriptionPic8 = product['descriptionPic8']
    except Exception as e:
        descriptionPic8 = ''

    try:
        descriptionPic9 = product['descriptionPic9']
    except Exception as e:
        descriptionPic9 = ''

    try:
        descriptionPic10 = product['descriptionPic10']
    except Exception as e:
        descriptionPic10 = ''

    try:
        descriptionPic11 = product['descriptionPic11']
    except Exception as e:
        descriptionPic11 = ''

    try:
        descriptionPic12 = product['descriptionPic12']
    except Exception as e:
        descriptionPic12 = ''

    try:
        descriptionPic13 = product['descriptionPic13']
    except Exception as e:
        descriptionPic13 = ''

    try:
        descriptionPic14 = product['descriptionPic14']
    except Exception as e:
        descriptionPic14 = ''

    try:
        descriptionPic15 = product['descriptionPic15']
    except Exception as e:
        descriptionPic15 = ''

    try:
        descriptionPic16 = product['descriptionPic16']
    except Exception as e:
        descriptionPic16 = ''

    product_info_array = [productId, productName, productAliasName, productBrand,
                keyWord, productType, productCode,
                productStyle, productMaterial, productSpace, importantParam,
                productCover, productPngPic,
                descriptionPic1, descriptionPic2, descriptionPic3,
                descriptionPic4, descriptionPic5, descriptionPic6,
                descriptionPic7, descriptionPic8, descriptionPic9,
                descriptionPic10, descriptionPic11, descriptionPic12,
                descriptionPic13, descriptionPic14, descriptionPic15,
                descriptionPic16]

    for i in range(len(product_info_array)):
        info = product_info_array[i]
        sheet.write(1, i, info)  # 将产品信息写入表中

    # 保存工作簿
    wbk.save(product_dir + str(productId) + '_product_info.xls')


if __name__ == "__main__":

    # TODO 通过多线程获取数据，分10个线程
    # ready_download_product(1, 100)


    # 开始序号
    total_start = 15000
    # 结束
    total_end = 20000
    # 线程数
    thread_number = 20
    # 每个线程的下载数量
    thread_per_number = (int) ((total_end - total_start) / thread_number)

    for i in range(thread_number):
        start_index = i * thread_per_number + total_start
        end_index = (i+1) * thread_per_number + total_start
        # print('start_index', start_index, 'end_index', end_index)
        t = threading.Thread(target=ready_download_product, args=(start_index, end_index,))
        t.start()

    # # 总下载数
    # total_product = 5000
    # # 每个线程的下载数
    # thread_per_number = 1000
    #
    # for i in range( int(total_product / thread_per_number) ):
    #     start_index = i * thread_per_number
    #     end_index = (i+1) * thread_per_number
    #     t = threading.Thread(target=ready_download_product, args=(start_index, end_index,))
    #     t.start()



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


