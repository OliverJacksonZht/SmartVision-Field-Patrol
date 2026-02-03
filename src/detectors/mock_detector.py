"""
模拟病害检测器，用于离线测试和开发环境
"""

import random
import time
from datetime import datetime
from typing import Dict


class MockDiseaseDetector:
    """模拟病害检测器，用于离线测试"""

    def __init__(self):
        self.diseases_db = {
            "水稻": [
                {"name": "稻瘟病", "symptoms": "叶片有梭形病斑", "solution": "使用三环唑防治"},
                {"name": "纹枯病", "symptoms": "基部有云纹状病斑", "solution": "使用井冈霉素"},
                {"name": "白叶枯病", "symptoms": "叶片边缘枯黄", "solution": "使用叶枯唑"},
                {"name": "健康", "symptoms": "叶片绿色健康", "solution": "保持良好管理"}
            ],
            "小麦": [
                {"name": "锈病", "symptoms": "叶片有锈色粉状物", "solution": "使用粉锈宁"},
                {"name": "赤霉病", "symptoms": "穗部有粉红色霉层", "solution": "使用多菌灵"},
                {"name": "健康", "symptoms": "植株健康，长势良好", "solution": "保持当前管理"}
            ],
            "玉米": [
                {"name": "玉米大斑病", "symptoms": "叶片出现大型黄褐色病斑", "solution": "使用代森锰锌"},
                {"name": "玉米锈病", "symptoms": "叶片有橙黄色粉状孢子堆", "solution": "使用三唑酮"},
                {"name": "健康", "symptoms": "植株健壮，叶片浓绿", "solution": "正常管理"}
            ]
        }

    def detect(self, image_path: str, crop_type: str = "水稻") -> Dict:
        """
        模拟检测过程

        Args:
            image_path: 图片路径（本检测器不实际读取图片）
            crop_type: 作物类型

        Returns:
            Dict: 检测结果字典
        """
        # 确保作物类型在数据库中
        if crop_type not in self.diseases_db:
            crop_type = "水稻"

        crop_diseases = self.diseases_db[crop_type]

        # 30%概率返回健康
        if random.random() < 0.3:
            healthy = next((d for d in crop_diseases if d["name"] == "健康"), crop_diseases[0])
            severity = "无" if healthy["name"] == "健康" else "轻微"
            disease = healthy
            confidence = random.uniform(0.8, 0.95)
        else:
            # 排除健康选项
            disease_options = [d for d in crop_diseases if d["name"] != "健康"]
            if not disease_options:
                disease_options = crop_diseases

            disease = random.choice(disease_options)
            severity = random.choice(["轻微", "中等", "严重"])
            confidence = random.uniform(0.6, 0.9)

        # 添加随机延迟模拟API调用
        time.sleep(random.uniform(1, 2))

        result = f"""
病害识别：{disease['name']}
症状描述：{disease['symptoms']}
严重程度：{severity}
置信度：{confidence:.2%}
建议措施：{disease['solution']}
检测时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
【注意：此为模拟数据，仅供参考】"""

        return {
            "status": "success",
            "mode": "mock",
            "result": result,
            "details": {
                "disease": disease['name'],
                "severity": severity,
                "confidence": round(confidence, 4),
                "solution": disease['solution'],
                "symptoms": disease['symptoms']
            }
        }