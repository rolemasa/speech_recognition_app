# -*- coding: utf-8 -*-
"""
音声録音機能を管理するモジュール
"""

import pyaudio
import threading
import queue
import time
from ..utils.config import Config

class AudioRecorder:
    """音声録音を管理するクラス"""
    
    def __init__(self):
        # PyAudio設定
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        
        # 録音状態
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
        # コールバック関数
        self.on_audio_data = None  # 音声データ受信時のコールバック
        self.on_error = None       # エラー発生時のコールバック
    
    def set_callbacks(self, on_audio_data=None, on_error=None):
        """
        コールバック関数を設定
        
        Args:
            on_audio_data: 音声データ受信時に呼ばれる関数
            on_error: エラー発生時に呼ばれる関数
        """
        self.on_audio_data = on_audio_data
        self.on_error = on_error
    
    def start_recording(self):
        """録音開始"""
        if self.is_recording:
            return False
        
        try:
            # 音声ストリームを開く
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                stream_callback=self._audio_callback
            )
            
            self.is_recording = True
            self.stream.start_stream()
            
            # 音声処理スレッドを開始
            self.processing_thread = threading.Thread(target=self._process_audio_data)
            self.processing_thread.daemon = True
            self.processing_thread.start()
            
            return True
            
        except Exception as e:
            if self.on_error:
                self.on_error(f"録音開始エラー: {str(e)}")
            return False
    
    def stop_recording(self):
        """録音停止"""
        if not self.is_recording:
            return
        
        try:
            self.is_recording = False
            
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
                
        except Exception as e:
            if self.on_error:
                self.on_error(f"録音停止エラー: {str(e)}")
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """
        PyAudioのコールバック関数
        音声データを受信したときに呼ばれる
        """
        if self.is_recording:
            self.audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)
    
    def _process_audio_data(self):
        """音声データを処理するスレッド"""
        audio_buffer = []
        last_process_time = time.time()
        
        while self.is_recording:
            try:
                # キューから音声データを取得
                audio_data = self.audio_queue.get(timeout=0.1)
                audio_buffer.append(audio_data)
                
                # 一定時間ごとまたは一定量たまったら処理
                current_time = time.time()
                if (current_time - last_process_time >= Config.PHRASE_TIME_LIMIT or 
                    len(audio_buffer) >= 50):  # 約1秒分
                    
                    if audio_buffer and self.on_audio_data:
                        combined_data = b''.join(audio_buffer)
                        self.on_audio_data(combined_data)
                    
                    audio_buffer = []
                    last_process_time = current_time
                    
            except queue.Empty:
                # キューが空の場合は継続
                continue
            except Exception as e:
                if self.on_error:
                    self.on_error(f"音声処理エラー: {str(e)}")
                break
    
    def is_microphone_available(self):
        """マイクが利用可能かチェック"""
        try:
            # 一時的にストリームを開いてテスト
            test_stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            test_stream.close()
            return True
        except Exception:
            return False
    
    def get_input_devices(self):
        """利用可能な入力デバイス一覧を取得"""
        devices = []
        try:
            for i in range(self.audio.get_device_count()):
                device_info = self.audio.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': device_info['name'],
                        'sample_rate': int(device_info['defaultSampleRate'])
                    })
        except Exception as e:
            if self.on_error:
                self.on_error(f"デバイス取得エラー: {str(e)}")
        
        return devices
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        self.stop_recording()
        if self.audio:
            self.audio.terminate()