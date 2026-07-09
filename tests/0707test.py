from flask import Flask, request, render_template_string, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

# ------------------- 前端 HTML 页面（嵌入在这里） -------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>电商产品图生成器</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
        .container { display: flex; gap: 30px; max-width: 1200px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .left-panel { flex: 1; }
        .right-panel { flex: 1; }
        .upload-box { border: 2px dashed #ccc; padding: 30px; text-align: center; border-radius: 12px; margin-bottom: 15px; cursor: pointer; transition: 0.3s; }
        .upload-box:hover { border-color: #409EFF; background: #f0f7ff; }
        .upload-box img { max-width: 100%; max-height: 150px; margin-top: 10px; }
        .upload-box input { display: none; }
        input, textarea { width: 100%; padding: 10px; margin-bottom: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; box-sizing: border-box; }
        textarea { height: 80px; resize: vertical; }
        .btn { background: #409EFF; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-size: 18px; cursor: pointer; width: 100%; transition: 0.3s; }
        .btn:hover { background: #66b1ff; }
        .right-panel img { max-width: 100%; border-radius: 12px; border: 1px solid #eee; }
        .preview-area { min-height: 400px; background: #fafafa; border-radius: 12px; display: flex; align-items: center; justify-content: center; }
        .status { margin-top: 10px; color: #999; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-panel">
            <h2>📤 步骤1：上传图片</h2>
            <div class="upload-box" id="templateBox">
                <p>🖼️ 点击或拖拽上传 <strong>参考模板图</strong></p>
                <img id="templatePreview" style="display:none;">
                <input type="file" id="templateInput" accept="image/*">
            </div>
            <div class="upload-box" id="productBox">
                <p>📦 点击或拖拽上传 <strong>产品图片</strong></p>
                <img id="productPreview" style="display:none;">
                <input type="file" id="productInput" accept="image/*">
            </div>

            <h2>✏️ 步骤2：编辑文字信息</h2>
            <input type="text" id="productTitle" placeholder="产品标题，例如：夏季新款连衣裙" value="夏季新款连衣裙">
            <input type="text" id="productPrice" placeholder="价格，例如：￥299" value="￥299">
            <input type="text" id="promoInfo" placeholder="促销信息，例如：限时8折" value="限时8折">
            <textarea id="sellingPoints" placeholder="卖点描述，例如：透气面料、修身显瘦">透气面料、修身显瘦</textarea>

            <button class="btn" id="generateBtn">🎨 生成图片</button>
            <div id="statusMsg" class="status">请上传图片并点击生成</div>
        </div>
        <div class="right-panel">
            <h2>✨ 生成结果预览</h2>
            <div class="preview-area">
                <img id="resultImage" src="" alt="生成的图片将在此处预览" style="max-height:500px;">
            </div>
        </div>
    </div>

    <script>
        // 上传预览逻辑
        function setupUpload(boxId, inputId, previewId) {
            const box = document.getElementById(boxId);
            const input = document.getElementById(inputId);
            const preview = document.getElementById(previewId);

            box.addEventListener('click', () => input.click());
            box.addEventListener('dragover', (e) => { e.preventDefault(); box.style.borderColor = '#409EFF'; });
            box.addEventListener('dragleave', () => { box.style.borderColor = '#ccc'; });
            box.addEventListener('drop', (e) => {
                e.preventDefault();
                box.style.borderColor = '#ccc';
                if (e.dataTransfer.files.length) {
                    input.files = e.dataTransfer.files;
                    handleFile(input, preview);
                }
            });
            input.addEventListener('change', () => handleFile(input, preview));
        }

        function handleFile(input, preview) {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }

        setupUpload('templateBox', 'templateInput', 'templatePreview');
        setupUpload('productBox', 'productInput', 'productPreview');

        // 点击生成 -> 调用后端 Flask API
        document.getElementById('generateBtn').addEventListener('click', async function() {
            const status = document.getElementById('statusMsg');
            status.innerText = '⏳ 正在生成，请稍候...';

            const formData = new FormData();
            const templateFile = document.getElementById('templateInput').files[0];
            const productFile = document.getElementById('productInput').files[0];

            if (!templateFile || !productFile) {
                status.innerText = '❌ 请先上传模板图和产品图！';
                return;
            }

            formData.append('template', templateFile);
            formData.append('product', productFile);
            formData.append('title', document.getElementById('productTitle').value);
            formData.append('price', document.getElementById('productPrice').value);
            formData.append('promo', document.getElementById('promoInfo').value);
            formData.append('desc', document.getElementById('sellingPoints').value);

            try {
                const response = await fetch('/generate', { method: 'POST', body: formData });
                if (!response.ok) throw new Error('生成失败');
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                document.getElementById('resultImage').src = url;
                status.innerText = '✅ 生成成功！';
            } catch (error) {
                status.innerText = '❌ 错误：' + error.message;
            }
        });
    </script>
</body>
</html>
"""


# ------------------- 后端图片合成逻辑 -------------------
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/generate', methods=['POST'])
def generate_image():
    # 1. 接收图片和文字
    template_file = request.files['template']
    product_file = request.files['product']
    title = request.form.get('title', '默认标题')
    price = request.form.get('price', '￥99')
    promo = request.form.get('promo', '限时优惠')
    desc = request.form.get('desc', '优质面料')

    # 2. 打开图片并转为 RGBA（支持透明背景）
    template = Image.open(template_file.stream).convert('RGBA')
    product = Image.open(product_file.stream).convert('RGBA')

    # 3. 调整产品图大小（保持宽高比，设定最大宽300，高300）
    product.thumbnail((300, 300), Image.LANCZOS)

    # 计算居中位置（放在模板偏下位置，可自行调整）
    x = (template.width - product.width) // 2
    y = template.height - product.height - 100  # 底部留白100px

    # 粘贴产品图（第三个参数使用自身作为蒙版，保留透明背景）
    template.paste(product, (x, y), product)

    # 4. 绘制文字
    draw = ImageDraw.Draw(template)

    # 加载中文字体（如果没有 simhei.ttf，会使用默认字体，但中文会显示为方框）
    font_path = "simhei.ttf"
    try:
        font_title = ImageFont.truetype(font_path, 36)
        font_price = ImageFont.truetype(font_path, 52)
        font_desc = ImageFont.truetype(font_path, 28)
    except:
        # 如果找不到字体，用默认字体（仅支持英文，中文会乱码）
        font_title = ImageFont.load_default()
        font_price = ImageFont.load_default()
        font_desc = ImageFont.load_default()
        print("⚠️ 警告：未找到 simhei.ttf 字体，中文可能显示为方框。请下载字体文件放在同目录下。")

    # 写标题（居中）
    text_width = draw.textlength(title, font=font_title)
    title_x = (template.width - text_width) // 2
    draw.text((title_x, 30), title, font=font_title, fill=(0, 0, 0, 255))

    # 写价格（居右，红色）
    price_width = draw.textlength(price, font=font_price)
    price_x = template.width - price_width - 40
    draw.text((price_x, 100), price, font=font_price, fill=(255, 0, 0, 255))

    # 写促销和卖点（居中，灰色）
    desc_text = f"{promo} | {desc}"
    desc_width = draw.textlength(desc_text, font=font_desc)
    desc_x = (template.width - desc_width) // 2
    draw.text((desc_x, template.height - 50), desc_text, font=font_desc, fill=(80, 80, 80, 255))

    # 5. 返回生成的图片
    img_io = io.BytesIO()
    template.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')


if __name__ == '__main__':
    # 让 Flask 允许外部访问（方便手机/其他设备测试）
    app.run(host='0.0.0.0', port=5001, debug=True)