"""
通义千问真实API检测器
"""

import base64
import os
import time
import requests
from typing import Dict, Optional


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
        """
        将图片转换为base64编码

        Args:
            image_path: 图片路径

        Returns:
            Optional[str]: base64编码的图片，失败返回None
        """
        try:
            if not os.path.exists(image_path):
                return None

            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
            return encoded
        except Exception:
            return None

    def create_prompt(self, crop_type: str = "水稻") -> str:
        """
        创建病害识别提示词

        Args:
            crop_type: 作物类型

        Returns:
            str: 提示词
        """
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
        """
        调用通义千问API进行病害识别

        Args:
            image_path: 图片路径
            crop_type: 作物类型

        Returns:
            Dict: 检测结果字典
        """
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

                    # 提取结构化信息
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
        """
        从API返回文本中提取结构化信息

        Args:
            text: API返回的文本
            crop_type: 作物类型

        Returns:
            Dict: 结构化的详细信息
        """
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