"""
病害检测器模块
"""

from .mock_detector import MockDiseaseDetector
from .qwen_detector import QwenDiseaseDetector
from .hybrid_detector import HybridDiseaseDetector

__all__ = [
    'MockDiseaseDetector',
    'QwenDiseaseDetector',
    'HybridDiseaseDetector'
]