"""
混合病害检测器：优先使用真实API，失败时使用模拟
"""

import json
from typing import Dict, Optional

from .mock_detector import MockDiseaseDetector
from .qwen_detector import QwenDiseaseDetector


class HybridDiseaseDetector:
    """混合病害检测器：优先使用真实API，失败时使用模拟"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.use_real_api = bool(api_key)

        # 初始化两个检测器
        self.qwen_detector = QwenDiseaseDetector(api_key) if api_key else None
        self.mock_detector = MockDiseaseDetector()

        # 统计信息
        self.stats = {
            "total_calls": 0,
            "success_calls": 0,
            "mock_calls": 0,
            "api_calls": 0,
            "avg_response_time": 0
        }

    def detect(self, image_path: str, crop_type: str = "水稻", force_mock: bool = False) -> Dict:
        """
        病害检测主函数

        Args:
            image_path: 图片路径
            crop_type: 作物类型
            force_mock: 强制使用模拟数据（即使有API key）

        Returns:
            Dict: 检测结果字典
        """
        self.stats["total_calls"] += 1

        # 强制使用模拟数据
        if force_mock:
            print("🔄 强制使用模拟检测模式")
            self.stats["mock_calls"] += 1
            return self.mock_detector.detect(image_path, crop_type)

        # 如果有API key，尝试调用真实API
        if self.use_real_api and self.qwen_detector:
            print(f"🔗 尝试调用通义千问API...")
            self.stats["api_calls"] += 1

            result = self.qwen_detector.detect(image_path, crop_type)

            if result["status"] == "success":
                self.stats["success_calls"] += 1
                print("✅ API调用成功")
                return result
            else:
                # API调用失败，回退到模拟
                print(f"⚠️  API调用失败，使用模拟数据: {result.get('error', '未知错误')}")
                self.stats["mock_calls"] += 1
                mock_result = self.mock_detector.detect(image_path, crop_type)
                mock_result["api_error"] = result.get("error")  # 记录API错误信息
                return mock_result
        else:
            # 没有API key，使用模拟数据
            print("🔌 无API key，使用模拟检测模式")
            self.stats["mock_calls"] += 1
            return self.mock_detector.detect(image_path, crop_type)

    def get_stats(self) -> Dict:
        """
        获取统计信息

        Returns:
            Dict: 统计信息字典
        """
        if self.stats["total_calls"] > 0:
            success_rate = (self.stats["success_calls"] / self.stats["total_calls"]) * 100
        else:
            success_rate = 0

        return {
            **self.stats,
            "success_rate": round(success_rate, 2),
            "api_available": self.use_real_api
        }

    def save_result_to_file(self, result: Dict, filename: str = "detection_result.json") -> bool:
        """
        保存检测结果到文件

        Args:
            result: 检测结果字典
            filename: 保存的文件名

        Returns:
            bool: 保存是否成功
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"💾 结果已保存到: {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存结果失败: {e}")
            return False