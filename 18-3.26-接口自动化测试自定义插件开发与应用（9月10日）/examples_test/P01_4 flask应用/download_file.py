from flask import Flask, send_file, abort
import os

app = Flask(__name__)


# download_file.py
@app.route('/download/<filename>')
def download_file(filename):
    # 1. 拼接文件路径：将 "img" 文件夹和文件名组合
    # 例如：filename="1.png" → file_path="img/1.png"
    file_path = os.path.join("img", filename)
    # 2. 检查文件是否存在
    if not os.path.exists(file_path):
        # 如果文件不存在，返回404错误
        abort(404, description="File not found")

    # 3. 发送文件给客户端
    return send_file(
        file_path,    # 要发送的文件路径
        as_attachment=True,   # 作为附件下载（弹出下载框）
        download_name=filename  # 保持原始文件名
    )


if __name__ == '__main__':
    app.run(debug=True, port=5001)  # 修改端口避免冲突