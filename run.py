"""
慧眼巡田 - 命令行运行入口
"""

import os
import sys
from typing import List

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.detectors import HybridDiseaseDetector


def main():
    """主测试函数"""
    print("=" * 60)
    print("🌾 智慧农业病害检测系统")
    print("=" * 60)

    # 初始化配置
    Config.init_directories()

    # 创建混合检测器
    detector = HybridDiseaseDetector(api_key=Config.QWEN_API_KEY)

    # 测试图片路径
    test_images = [
        os.path.join(Config.TEST_IMAGES_DIR, "test_rice.jpg"),      # 水稻测试图片
        os.path.join(Config.TEST_IMAGES_DIR, "farm_field.jpg"),
        os.path.join(Config.TEST_IMAGES_DIR, "wheat_disease.jpg"),
    ]

    # 查找存在的图片
    available_images = []
    for img in test_images:
        if os.path.exists(img):
            available_images.append(img)
        else:
            print(f"⚠️  图片不存在: {img}")

    if not available_images:
        print("❌ 没有找到任何测试图片！")
        print("请创建以下图片文件之一：")
        for img in test_images:
            print(f"  - {img}")
        return

    print(f"📁 找到 {len(available_images)} 张测试图片")

    # 测试每张图片
    for i, image_path in enumerate(available_images, 1):
        print(f"\n{'='*50}")
        print(f"测试 [{i}/{len(available_images)}]: {os.path.basename(image_path)}")

        # 根据文件名猜测作物类型
        if "rice" in image_path.lower():
            crop_type = "水稻"
        elif "wheat" in image_path.lower():
            crop_type = "小麦"
        elif "corn" in image_path.lower() or "maize" in image_path.lower():
            crop_type = "玉米"
        else:
            crop_type = "水稻"  # 默认

        # 进行检测
        result = detector.detect(
            image_path=image_path,
            crop_type=crop_type,
            force_mock=False
        )

        # 显示结果
        print(f"\n🌱 作物类型: {crop_type}")
        print(f"📊 检测模式: {result.get('mode', 'unknown')}")

        if result["status"] == "success":
            print("✅ 检测成功！")
            print("-" * 40)
            print(result["result"])
            print("-" * 40)

            # 显示详细信息
            details = result.get("details", {})
            if details:
                print("\n📋 结构化信息:")
                for key, value in details.items():
                    print(f"  {key}: {value}")

            # 保存结果
            save_file = os.path.join(
                Config.RESULTS_DIR,
                f"result_{os.path.splitext(os.path.basename(image_path))[0]}.json"
            )
            detector.save_result_to_file(result, save_file)
        else:
            print(f"❌ 检测失败: {result.get('error', '未知错误')}")

    # 显示统计信息
    print(f"\n{'='*50}")
    print("📈 检测统计:")
    stats = detector.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 50)
    print("🔧 系统状态:")
    if detector.use_real_api:
        print("✅ 通义千问API: 已配置")
        print(f"📡 成功调用: {stats['success_calls']}/{stats['api_calls']} 次")
    else:
        print("⚠️  通义千问API: 未配置 (使用模拟模式)")
        print("💡 提示: 设置 QWEN_API_KEY 环境变量以使用真实API")


def test_api_only():
    """仅测试API连接"""
    print("🧪 测试通义千问API连接...")

    if not Config.QWEN_API_KEY:
        print("⚠️  未配置 API Key")
        return

    # 简单的API测试
    url = f"{Config.QWEN_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {Config.QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen-max",
        "messages": [
            {
                "role": "user",
                "content": "你好，简单测试一下"
            }
        ],
        "max_tokens": 10
    }

    try:
        print("发送测试请求...")
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        response = requests.post(url, headers=headers, json=data, verify=False, timeout=10)

        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ API连接成功！")
            print(f"响应: {response.json()}")
        elif response.status_code == 401:
            print("❌ API Key无效或过期")
        else:
            print(f"❌ API错误: {response.text[:200]}")
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("💡 可能的原因:")
        print("  1. 网络连接问题")
        print("  2. API Key无效")
        print("  3. 服务器SSL证书问题")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_api_only()
        elif sys.argv[1] == "mock":
            # 仅使用模拟模式测试
            print("🧪 模拟模式测试...")
            detector = HybridDiseaseDetector(api_key=None)
            Config.init_directories()
            test_image = os.path.join(Config.TEST_IMAGES_DIR, "test_rice.jpg")
            if os.path.exists(test_image):
                result = detector.detect(test_image, "水稻", force_mock=True)
                print(result["result"])
            else:
                print("❌ 测试图片不存在")
        else:
            main()
    else:
        main()