# 导入图片处理模块PIL
from PIL import Image
# 导入OCR文字识别库
import pytesseract
import os  # 新增：打印当前目录用来排查路径

def get_image_text(img_path=r'/Users/temu/PycharmProjects/pythonProject/data/test_picture.jpeg', lang="chi_sim+eng"):
    """
    读取本地图片中的文字
    :param img_path: 本地图片路径
    :param lang: 识别语言，chi_sim简体中文+eng英文
    :return: 返回识别出的文本字符串
    """
    # =========重要=========
    # 你是Mac系统，直接注释下面这一行，不要填图片路径！
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    try:
        # 打开图片文件
        img = Image.open(img_path)
        # OCR识别图片文字
        text_result = pytesseract.image_to_string(
            image=img,
            lang=lang
        )
        return text_result
    except FileNotFoundError:
        return f"报错：未找到图片文件，路径[{img_path}]不存在"
    except Exception as error:
        return f"识别失败，异常详情：{str(error)}"

# 程序运行入口
if __name__ == "__main__":
    # 打印当前运行文件夹，方便你确认路径
    print("程序当前工作目录：", os.getcwd())

    # 脚本在tests文件夹，图片在上一级目录，固定写这个路径
    picture_path = "../test_picture.jpeg"

    # 调用识别函数
    ocr_text = get_image_text(picture_path)

    # 打印识别结果
    print("=====图片文字识别结果=====")
    print(ocr_text)

    # 将识别文字保存到txt文件（生成在tests文件夹内）
    with open("图片识别输出.txt", "w", encoding="utf-8") as f:
        f.write(ocr_text)
    print("\n识别内容已保存到【图片识别输出.txt】")