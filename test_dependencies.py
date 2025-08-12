#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
依存関係テストスクリプト
必要なライブラリが正しくインストールされているかチェック
"""

def test_dependencies():
    """依存関係をテストする"""
    print("=" * 50)
    print("依存関係テスト開始")
    print("=" * 50)
    
    tests = []
    
    # tkinter テスト
    try:
        import tkinter as tk
        # 簡単なウィンドウを作成してすぐ閉じる
        root = tk.Tk()
        root.withdraw()
        root.destroy()
        tests.append(("tkinter", "✅ OK", "標準ライブラリ"))
    except ImportError as e:
        tests.append(("tkinter", "❌ エラー", str(e)))
    
    # speech_recognition テスト
    try:
        import speech_recognition as sr
        version = getattr(sr, '__version__', 'バージョン不明')
        tests.append(("speech_recognition", "✅ OK", f"バージョン: {version}"))
    except ImportError as e:
        tests.append(("speech_recognition", "❌ エラー", str(e)))
    
    # pyaudio テスト
    try:
        import pyaudio
        version = getattr(pyaudio, '__version__', 'バージョン不明')
        tests.append(("pyaudio", "✅ OK", f"バージョン: {version}"))
    except ImportError as e:
        tests.append(("pyaudio", "❌ エラー", str(e)))
    
    # datetime テスト（標準ライブラリ）
    try:
        import datetime
        tests.append(("datetime", "✅ OK", "標準ライブラリ"))
    except ImportError as e:
        tests.append(("datetime", "❌ エラー", str(e)))
    
    # os テスト（標準ライブラリ）
    try:
        import os
        tests.append(("os", "✅ OK", "標準ライブラリ"))
    except ImportError as e:
        tests.append(("os", "❌ エラー", str(e)))
    
    # threading テスト（標準ライブラリ）
    try:
        import threading
        tests.append(("threading", "✅ OK", "標準ライブラリ"))
    except ImportError as e:
        tests.append(("threading", "❌ エラー", str(e)))
    
    # 結果表示
    print(f"{'ライブラリ名':<20} {'状態':<10} {'詳細'}")
    print("-" * 50)
    
    all_ok = True
    for lib_name, status, details in tests:
        print(f"{lib_name:<20} {status:<10} {details}")
        if "❌" in status:
            all_ok = False
    
    print("=" * 50)
    
    if all_ok:
        print("✅ すべての依存関係が正常です！")
        print("アプリケーションを起動できます:")
        print("python main.py")
    else:
        print("❌ 一部の依存関係でエラーがあります。")
        print("\n解決方法:")
        
        for lib_name, status, details in tests:
            if "❌" in status:
                if lib_name == "tkinter":
                    print(f"\n{lib_name}:")
                    print("  Ubuntu/Debian: sudo apt-get install python3-tk")
                    print("  CentOS/RHEL: sudo yum install tkinter")
                    print("  macOS: tkinterは通常プリインストール済み")
                    print("  Windows: tkinterは通常プリインストール済み")
                
                elif lib_name == "pyaudio":
                    print(f"\n{lib_name}:")
                    print("  Windows: pip install pipwin && pipwin install pyaudio")
                    print("  macOS: brew install portaudio && pip install pyaudio")
                    print("  Linux: sudo apt-get install python3-pyaudio")
                
                elif lib_name == "speech_recognition":
                    print(f"\n{lib_name}:")
                    print("  pip install SpeechRecognition")
    
    print("=" * 50)
    
    # マイクロフォンテスト（pyaudioが利用可能な場合）
    if all_ok:
        test_microphone()

def test_microphone():
    """マイクロフォンの動作テスト"""
    print("\nマイクロフォンテスト開始...")
    
    try:
        import pyaudio
        
        # PyAudioインスタンス作成
        audio = pyaudio.PyAudio()
        
        print("利用可能な音声入力デバイス:")
        input_devices = []
        
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                input_devices.append({
                    'index': i,
                    'name': device_info['name'],
                    'sample_rate': int(device_info['defaultSampleRate'])
                })
                print(f"  [{i}] {device_info['name']} (サンプルレート: {int(device_info['defaultSampleRate'])}Hz)")
        
        if input_devices:
            print(f"✅ {len(input_devices)}個のマイクデバイスが見つかりました")
            
            # デフォルトデバイスでテスト録音
            try:
                test_stream = audio.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024
                )
                test_stream.close()
                print("✅ マイクロフォンのテスト録音に成功しました")
                
            except Exception as e:
                print(f"❌ マイクロフォンのテスト録音に失敗: {e}")
                print("  マイクの接続とアクセス許可を確認してください")
        else:
            print("❌ 利用可能なマイクデバイスが見つかりません")
        
        audio.terminate()
        
    except Exception as e:
        print(f"❌ マイクロフォンテストエラー: {e}")

if __name__ == "__main__":
    test_dependencies()