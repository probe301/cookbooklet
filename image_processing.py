

def crop_image(input, output, left, top, right, bottom):
    # 读取和裁剪图像
    # path = f'../path/subpath/test.jpg'
    # crop_image(path, 'tmp.jpg', 200, 200, 1500, 2500)
    from PIL import Image
    import matplotlib.pyplot as plt
    img = Image.open(input)

    # # 裁剪图像
    # width, height = img.size
    # left = (width - 300) / 2
    # top = (height - 300) / 2
    # right = (width + 300) / 2
    # bottom = (height + 300) / 2
    img = img.crop((left, top, right, bottom))

    # 显示图像 in notebook
    plt.imshow(img)
    plt.show()
    img.save(output)
    return True





def fitz_crop_pdf_page(page_num):
    '''读取 PDF 并裁剪指定页面的坐标区域，你可以使用 PyPDF2 或 PyMuPDF 这类 PDF 处理库。下面是一个使用 PyMuPDF 的示例代码，其中 page_num 变量指定了要裁剪的页面编号，x1，y1，x2，y2 变量指定了要裁剪的矩形区域的左上角和右下角坐标： #viaPoe'''
    import fitz  # fitz = PyMuPDF

    doc = fitz.open('example.pdf')
    # 获取指定页面
    page = doc[page_num]

    # The page's /CropBox for a PDF.
    # Always the unrotated page rectangle is returned. For a non-PDF this will always equal the page rectangle.
    # r = page.rect
    # str(page.cropbox)

    # 裁剪指定区域
    rect0 = fitz.Rect(0, 0, 1000, 1425)
    
    # fitz.Matrix(300/72, 300/72) 可以提升出图质量
    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), clip=rect0)
    
    pix = page.get_pixmap(clip=rect0)
    pix.save('output.png')



### OCR
import pathlib
import requests

# 剩余次数 https://console.bce.baidu.com/ai/#/ai/ocr/overview/index

API_KEY = "qzD...dx8"                     # 创建app后获取
SECRET_KEY = "aMM...vRlX"

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def get_baidu_ocr_url(kind='accurate'):
    # 高精度含位置   高精度            标准含位置    标准
    # 'accurate',  'accurate_basic', 'general',   'general_basic'
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/{kind}?access_token=" + get_access_token()
    return url

# 高精度版 总体上文字细节质量强,
# 但可能反而把某些字认出错, (即使在标准版里都能识别)
# 且会丢弃不认识的字 调req参数?
ACCU_OCR_URL = get_baidu_ocr_url('accurate')
# 标准版 质量差些 文字似乎没用到上下文联系推断
BASIC_OCR_URL = get_baidu_ocr_url('general')


import base64
import urllib
import requests
def get_file_content_as_base64(path, urlencoded=False):
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def baidu_ocr_one_page(url, image_path) -> dict:
    assert pathlib.Path(image_path).exists()
    image_code = get_file_content_as_base64(image_path, True)
    payload= f'image={image_code}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return pylon.json_loads(response.text)  # a dict

def baidu_ocr_one_page_merge_txt(data):
    return  '\n'.join(block.get('words', '') for block in data.get('words_result', []))

def baidu_ocr_one_page_save(image_path, data, overwrite=True):
    result_json = data
    result_txt = baidu_ocr_one_page_merge_txt(data)
    result_txt_path = image_path.replace('.jpg', '.txt')
    result_json_path = image_path.replace('.jpg', '.json')
    if overwrite == False:
        assert not pathlib.Path(result_txt_path).exists()
        assert not pathlib.Path(result_json_path).exists()
    # pylon.text_save(result_txt_path, result_txt)
    # pylon.json_save(path=result_json_path, data=result_json)
    # print(f'save to {result_txt_path} {result_json_path} done')





def pdf_extract_text():
    '''从已经是文字的pdf里提取'''

    import pdfplumber
    PDF_PATH = './books/xxx.pdf'
    with pdfplumber.open(PDF_PATH) as pdf:
        first_page = pdf.pages[0]
        choice_page = pdf.pages[55]
        first_page.chars[0]     # | logi
        choice_page.chars[8]    # | logi
        choice_page.extract_words()
        # [ {'text': '第', 'x0': 42.51, 'x1': 51.51, 'top': 49.579, 'doctop': 28892.12, 'bottom': 58.579, 'upright': True, 'direction': 1},
        #   {'text': '三', 'x0': 65.011, 'x1': 74.011, 'top': 49.579, 'doctop': 28892.12, 'bottom': 58.579, 'upright': True, 'direction': 1},
        #   {'text': '回', 'x0': 87.511, 'x1': 96.511, 'top': 49.579, 'doctop': 28892.12, 'bottom': 58.579, 'upright': True, 'direction': 1}, ...]
