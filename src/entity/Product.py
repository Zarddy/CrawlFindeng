

# 产品数据信息
class Product:

    def __init__(self, productId, productName, productAliasName, productBrand,
                 productCover, productPngPic, descriptionPic, keyWord, productType,
                 productCode, productStyle, productMaterial, productSpace, importantParam):

        self.productId = productId # 产品id
        self.productName = productName # 产品名称
        self.productAliasName = productAliasName # 产品别名
        self.productBrand = productBrand # 品牌

        self.productCover = productCover # 封面图
        self.productPngPic = productPngPic # 配灯图
        self.descriptionPic = descriptionPic # 产品详情图
        self.keyword = keyWord # 关键词
        self.productType = productType # 产品分类
        self.productCode = productCode # 产品代号
        self.productStyle = productStyle # 风格
        self.productMaterial = productMaterial # 材质
        self.productSpace = productSpace # 空间
        self.importantParam = importantParam # 其它参数

    def save_to_txt(self):
        try:
            f = open(self.product_dir + self.productId + '_product_data.txt', 'wb')
            f.write(str(self).encode("utf-8"))
            f.close
        except Exception as e:
            print(e)

    def save_to_xls(self):
        print('')
