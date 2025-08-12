# -*- coding: utf-8 -*-
"""
アプリケーションの設定を管理するモジュール
"""

import os

class Config:
    """アプリケーション設定クラス"""

    # アプリケーション情報
    APP_NAME = "音声文字起こしアプリ"
    APP_VERSION = "1.0.0"

    # ウィンドウ設定
    WINDOW_WIDTH = 700
    WINDOW_HEIGHT = 550
    WINDOW_MIN_WIDTH = 600
    WINDOW_MIN_HEIGHT = 450

    # 音声認識設定
    RECOGNITION_LANGUAGE = 'ja-JP' # 日本語
    RECOGNITION_TIMEOUT  = 1       # 音声待機タイムアウト（秒）
    PHRASE_TIME_LIMIT    = 5       # フレーズ時間制限（秒）

    # ディレクトリ設定
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
    TEMP_DIR = os.path.join(BASE_DIR, 'temp')

    # ファイル設定
    DEFAULT_SAVE_FORMAT = '.txt'
    SUPPORTED_FORMATS = [
        ("テキストファイル", "*.txt"),
        ("すべてのファイル", "*.*")
    ]

    # UI色設定
    COLORS = {
        'primary': '#2E7D32',      # 緑
        'secondary': '#1976D2',    # 青
        'success': '#4CAF50',      # 明るい緑
        'warning': '#FF9800',      # オレンジ
        'danger': '#F44336',       # 赤
        'info': '#2196F3',         # ライトブルー
        'light': '#F5F5F5',        # ライトグレー
        'dark': '#424242'          # ダークグレー
    }

    @classmethod
    def ensure_directories(cls):
        """必要なディレクトリを作成"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
