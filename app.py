"""
慧眼巡田 - Web服务入口
Flask Web应用，提供病害检测的Web界面
"""

import os
import json
import uuid
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.detectors import HybridDiseaseDetector


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_DIR

# 初始化配置
Config.init_directories()

# 创建检测器
detector = HybridDiseaseDetector(api_key=Config.QWEN_API_KEY)


@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/detect', methods=['POST'])
def detect_disease():
    """
    病害检测API接口

    接收参数：
    - file: 图片文件
    - crop_type: 作物类型（可选，默认为水稻）

    返回：
    - JSON格式的检测结果
    """
    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({
            'status': 'error',
            'message': '没有上传图片'
        }), 400

    file = request.files['file']

    # 检查文件名是否为空
    if file.filename == '':
        return jsonify({
            'status': 'error',
            'message': '未选择文件'
        }), 400

    # 检查文件类型
    if not Config.allowed_file(file.filename):
        return jsonify({
            'status': 'error',
            'message': f'不支持的文件格式，仅支持: {", ".join(Config.ALLOWED_EXTENSIONS)}'
        }), 400

    # 获取作物类型
    crop_type = request.form.get('crop_type', '水稻')

    # 保存上传的文件
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)

    try:
        # 进行检测
        result = detector.detect(filepath, crop_type)

        # 保存结果到results目录
        result_filename = f"result_{uuid.uuid4().hex}.json"
        result_filepath = os.path.join(Config.RESULTS_DIR, result_filename)
        with open(result_filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 返回结果
        return jsonify({
            'status': 'success',
            'data': {
                'result': result.get('result'),
                'mode': result.get('mode'),
                'details': result.get('details'),
                'crop_type': crop_type,
                'image_name': filename,
                'result_file': result_filename,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'检测失败: {str(e)}'
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取检测统计信息"""
    stats = detector.get_stats()
    return jsonify({
        'status': 'success',
        'data': stats
    })


@app.route('/results/<filename>')
def get_result(filename):
    """获取结果文件"""
    return send_from_directory(Config.RESULTS_DIR, filename)


@app.route('/uploads/<filename>')
def get_upload(filename):
    """获取上传的图片"""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)


@app.errorhandler(413)
def request_entity_too_large(error):
    """处理文件过大错误"""
    return jsonify({
        'status': 'error',
        'message': f'文件过大，最大支持 {Config.MAX_CONTENT_LENGTH // (1024*1024)}MB'
    }), 413


@app.errorhandler(500)
def internal_error(error):
    """处理内部错误"""
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🌾 慧眼巡田 - Web服务")
    print("=" * 60)
    print(f"📡 服务地址: http://{Config.HOST}:{Config.PORT}")
    print(f"📁 上传目录: {Config.UPLOAD_DIR}")
    print(f"📁 结果目录: {Config.RESULTS_DIR}")
    print("=" * 60)
    print("\n启动服务...")

    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )