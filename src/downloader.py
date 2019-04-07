import requests


def download_image(path, filename, url):
    response = requests.get(url=url)
    if response.status_code == 200:
        content = response.content

        image_path = path + filename
        f = open(image_path, 'wb')
        f.write(content)
        f.close


def download_image_with_prefix(path, prefix, url):
    # 如果路径为空
    if len(url) ==0 :
        return
    # 文件名称
    filename = prefix + str.split(url, '/')[-1]

    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            content = response.content

            image_path = path + filename
            f = open(image_path, 'wb')
            f.write(content)
            f.close
    except Exception as e:
        pass
