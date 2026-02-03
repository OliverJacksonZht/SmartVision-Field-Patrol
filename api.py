import requests
import base64
import json
import random
import os
import time
from datetime import datetime
from typing import Dict, Optional, Union
import urllib3
import warnings

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings('ignore')

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


class QwenDiseaseDetector:
    """通义千问真实API检测器"""
    def __init__(self, api_key: str, base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.endpoint = f"{base_url}/chat/completions"
        
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 请求超时设置（秒）
        self.timeout = 30
    
    def encode_image_to_base64(self, image_path: str) -> Optional[str]:
        """将图片转换为base64编码"""
        try:
            if not os.path.exists(image_path):
                return None
            
            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            return encoded
        except Exception:
            return None
    
    def create_prompt(self, crop_type: str = "水稻") -> str:
        """创建病害识别提示词"""
        return f"""你是一位资深农业专家，请分析这张{crop_type}的田间图像。

请按以下结构化格式返回病虫害识别结果：
1. **病害名称**：识别出的主要病害或虫害名称
2. **症状描述**：详细描述病害症状
3. **严重程度**：评估严重程度（轻微/中等/严重）
4. **置信度**：你对识别结果的置信度（0-100%）
5. **防治建议**：提供具体的防治措施和用药建议
6. **紧急程度**：处理紧急程度（低/中/高）

如果图像中未发现明显病虫害，请返回作物健康状况。

请用中文回答，确保建议专业、实用。"""
    
    def detect(self, image_path: str, crop_type: str = "水稻") -> Dict:
        """调用通义千问API进行病害识别"""
        # 1. 检查图片
        if not os.path.exists(image_path):
            return {
                "status": "error",
                "mode": "qwen",
                "error": f"图片不存在: {image_path}"
            }
        
        # 2. 编码图片
        image_base64 = self.encode_image_to_base64(image_path)
        if not image_base64:
            return {
                "status": "error",
                "mode": "qwen",
                "error": "图片编码失败"
            }
        
        # 3. 准备请求
        prompt = self.create_prompt(crop_type)
        payload = {
            "model": "qwen-vl-plus",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1500,
            "temperature": 0.1  # 较低温度使输出更稳定
        }
        
        try:
            print(f"🔍 调用通义千问API分析: {os.path.basename(image_path)}")
            start_time = time.time()
            
            # 发送请求（添加verify=False绕过SSL验证）
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
                verify=False
            )
            
            elapsed_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    answer = result["choices"][0]["message"]["content"]
                    
                    # 提取结构化信息（简单尝试）
                    details = self._extract_details(answer, crop_type)
                    
                    return {
                        "status": "success",
                        "mode": "qwen",
                        "result": answer,
                        "details": details,
                        "response_time": round(elapsed_time, 2),
                        "raw_response": result
                    }
                else:
                    return {
                        "status": "error",
                        "mode": "qwen",
                        "error": "API返回格式异常",
                        "raw_response": result
                    }
            else:
                return {
                    "status": "error",
                    "mode": "qwen",
                    "error": f"API调用失败 ({response.status_code}): {response.text[:200]}",
                    "response_time": round(elapsed_time, 2)
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "mode": "qwen",
                "error": f"请求超时 ({self.timeout}秒)"
            }
        except Exception as e:
            return {
                "status": "error", 
                "mode": "qwen",
                "error": f"请求异常: {str(e)}"
            }
    
    def _extract_details(self, text: str, crop_type: str) -> Dict:
        """从API返回文本中提取结构化信息"""
        details = {
            "disease": "未知",
            "severity": "未知",
            "confidence": 0.0,
            "solution": "未知",
            "symptoms": "未知"
        }
        
        # 简单关键词提取
        text_lower = text.lower()
        
        # 尝试提取病害名称
        disease_keywords = ["稻瘟病", "纹枯病", "白叶枯病", "锈病", "赤霉病", "大斑病", "霜霉病", "白粉病"]
        for disease in disease_keywords:
            if disease in text:
                details["disease"] = disease
                break
        
        # 提取严重程度
        if "严重" in text:
            details["severity"] = "严重"
        elif "中等" in text or "中度" in text:
            details["severity"] = "中等"
        elif "轻微" in text or "轻度" in text:
            details["severity"] = "轻微"
        
        # 提取置信度（如果有百分比）
        import re
        confidence_match = re.search(r'(\d+\.?\d*)%', text)
        if confidence_match:
            try:
                details["confidence"] = float(confidence_match.group(1)) / 100
            except:
                pass
        
        return details


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
        :param image_path: 图片路径
        :param crop_type: 作物类型
        :param force_mock: 强制使用模拟数据（即使有API key）
        :return: 检测结果字典
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
        """获取统计信息"""
        if self.stats["total_calls"] > 0:
            success_rate = (self.stats["success_calls"] / self.stats["total_calls"]) * 100
        else:
            success_rate = 0
            
        return {
            **self.stats,
            "success_rate": round(success_rate, 2),
            "api_available": self.use_real_api
        }
    
    def save_result_to_file(self, result: Dict, filename: str = "detection_result.json"):
        """保存检测结果到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"💾 结果已保存到: {filename}")
            return True
        except Exception as e:
            print(f"❌ 保存结果失败: {e}")
            return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("🌾 智慧农业病害检测系统")
    print("=" * 60)
    
    # 配置API Key（从环境变量或直接设置）
    API_KEY = os.getenv('QWEN_API_KEY', 'sk-36af5e3baa1e46239a130cc453dd8a77')
    
    # 创建混合检测器
    detector = HybridDiseaseDetector(api_key=API_KEY)
    
    # 测试图片路径（请确保图片存在）
    test_images = [
        "test_rice.jpg",      # 水稻测试图片
        "farm_field.jpg",     # 农田图片
        "wheat_disease.jpg",  # 小麦病害图片
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
            force_mock=False  # 设为True强制使用模拟数据
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
            save_file = f"result_{os.path.splitext(os.path.basename(image_path))[0]}.json"
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
    
    API_KEY = os.getenv('QWEN_API_KEY', 'sk-36af5e3baa1e46239a130cc453dd8a77')
    
    if not API_KEY or API_KEY == 'sk-36af5e3baa1e46239a130cc453dd8a77':
        print("⚠️  请使用有效的API Key")
        return
    
    # 简单的API测试
    url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
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
    # 测试选项
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_api_only()
        elif sys.argv[1] == "mock":
            # 仅使用模拟模式测试
            print("🧪 模拟模式测试...")
            detector = HybridDiseaseDetector(api_key=None)
            result = detector.detect("test_rice.jpg", "水稻", force_mock=True)
            print(result["result"])
        else:
            main()
    else:
        main()