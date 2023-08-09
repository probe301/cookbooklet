

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



# 要在 Python 中读取 PDF 并裁剪指定页面的坐标区域，你可以使用 PyPDF2 或 PyMuPDF 这类 PDF 处理库。下面是一个使用 PyMuPDF 的示例代码，其中 page_num 变量指定了要裁剪的页面编号，x1，y1，x2，y2 变量指定了要裁剪的矩形区域的左上角和右下角坐标： #viaPoe

def fitz_crop_pdf_page(page_num)
    import fitz  # fitz = PyMuPDF

    doc = fitz.open('example.pdf')
    # 获取指定页面
    page = doc[page_num]
    # 裁剪指定区域
    rect = fitz.Rect(x1, y1, x2, y2)
    pix = page.getPixmap(matrix=fitz.Matrix(), clip=rect)
    # 保存为图片文件
    pix.writePNG('output.png')


# 此代码将指定页面的指定矩形区域裁剪为一个图像，并将其保存为 PNG 文件。如果需要处理多个页面，可以使用循环遍历 doc 中的每个页面来进行处理。请注意，对于某些 PDF 文件，可能需要在 fitz.open() 中添加密码参数来打开文件
