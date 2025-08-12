#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
音声文字起こしアプリケーション
メインエントリーポイント
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def check_dependencies():
    """必要なライブラリがインストールされているかチェック"""
    missing_packages = []
    
    try:
        import speech_recognition as sr
    except ImportError:
        missing_packages.append("SpeechRecognition")
    
    try:
        import pyaudio
    except ImportError:
        missing_packages.append("pyaudio")
    
    if missing_packages:
        error_message = (
            "以下の必要なライブラリがインストールされていません:\n"
            f"{', '.join(missing_packages)}\n\n"
            "以下のコマンドでインストールしてください:\n"
            f"pip install {' '.join(missing_packages)}\n\n"
            "注意: pyaudioでエラーが発生する場合は以下も試してください:\n"
            "pip install pipwin\n"
            "pipwin install pyaudio"
        )
        
        # GUIでエラーメッセージを表示
        root = tk.Tk()
        root.withdraw()  # メインウィンドウを非表示
        messagebox.showerror("依存関係エラー", error_message)
        root.destroy()
        
        print("=" * 60)
        print("依存関係エラー")
        print("=" * 60)
        print(error_message)
        print("=" * 60)
        
        return False
    
    return True

def main():
    """メイン関数"""
    print("音声文字起こしアプリケーションを開始します...")
    
    # 依存関係をチェック
    if not check_dependencies():
        print("アプリケーションを終了します。")
        sys.exit(1)
    
    try:
        # メインウィンドウをインポートして実行
        from src.gui.main_window import MainWindow
        
        print("GUIを初期化しています...")
        app = MainWindow()
        
        print("アプリケーションを起動します。")
        app.run()
        
    except ImportError as e:
        error_message = f"モジュールのインポートエラー: {str(e)}"
        print(f"エラー: {error_message}")
        
        # GUIでエラーメッセージを表示
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("インポートエラー", error_message)
        root.destroy()
        
        sys.exit(1)
        
    except Exception as e:
        error_message = f"予期しないエラー: {str(e)}"
        print(f"エラー: {error_message}")
        
        # GUIでエラーメッセージを表示
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("エラー", error_message)
        root.destroy()
        
        sys.exit(1)

if __name__ == "__main__":
    main()