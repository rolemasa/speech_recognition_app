# -*- coding: utf-8 -*-
"""
音声認識機能を管理するモジュール
"""

import speech_recognition as sr
import io
import wave
import threading
from ..utils.config import Config

class SpeechRecognizer:
    """音声認識を管理するクラス"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # コールバック関数
        self.on_recognition_result = None  # 認識結果受信時のコールバック
        self.on_error = None               # エラー発生時のコールバック
        self.on_listening = None           # 音声待機開始時のコールバック
        
        # 認識設定
        self.language = Config.RECOGNITION_LANGUAGE
        
        # マイクロフォンの初期化
        self._initialize_microphone()
    
    def _initialize_microphone(self):
        """マイクロフォンを初期化"""
        try:
            self.microphone = sr.Microphone()
            # 環境音に合わせてマイクを調整
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            if self.on_error:
                self.on_error(f"マイク初期化エラー: {str(e)}")
    
    def set_callbacks(self, on_recognition_result=None, on_error=None, on_listening=None):
        """
        コールバック関数を設定
        
        Args:
            on_recognition_result: 認識結果受信時に呼ばれる関数
            on_error: エラー発生時に呼ばれる関数
            on_listening: 音声待機開始時に呼ばれる関数
        """
        self.on_recognition_result = on_recognition_result
        self.on_error = on_error
        self.on_listening = on_listening
    
    def recognize_from_microphone_once(self):
        """
        マイクから一度だけ音声認識を実行
        """
        def _recognize():
            try:
                if self.on_listening:
                    self.on_listening()
                
                with self.microphone as source:
                    # 音声を録音
                    audio_data = self.recognizer.listen(
                        source, 
                        timeout=Config.RECOGNITION_TIMEOUT,
                        phrase_time_limit=Config.PHRASE_TIME_LIMIT
                    )
                
                # Google音声認識を実行
                text = self.recognizer.recognize_google(
                    audio_data, 
                    language=self.language
                )
                
                if self.on_recognition_result:
                    self.on_recognition_result(text)
                    
            except sr.WaitTimeoutError:
                if self.on_error:
                    self.on_error("音声が検出されませんでした（タイムアウト）")
            except sr.UnknownValueError:
                if self.on_error:
                    self.on_error("音声を認識できませんでした")
            except sr.RequestError as e:
                if self.on_error:
                    self.on_error(f"音声認識サービスエラー: {str(e)}")
            except Exception as e:
                if self.on_error:
                    self.on_error(f"認識エラー: {str(e)}")
        
        # 別スレッドで実行
        thread = threading.Thread(target=_recognize)
        thread.daemon = True
        thread.start()
    
    def recognize_from_audio_data(self, audio_data, sample_rate=44100):
        """
        音声データから直接認識を実行
        
        Args:
            audio_data: 音声データ（バイト列）
            sample_rate: サンプリングレート
        """
        def _recognize():
            try:
                # 音声データをWAVフォーマットに変換
                audio_io = io.BytesIO()
                with wave.open(audio_io, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # モノラル
                    wav_file.setsampwidth(2)  # 16bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_data)
                
                audio_io.seek(0)
                
                # AudioFileとして読み込み
                with sr.AudioFile(audio_io) as source:
                    audio = self.recognizer.record(source)
                
                # Google音声認識を実行
                text = self.recognizer.recognize_google(
                    audio, 
                    language=self.language
                )
                
                if self.on_recognition_result:
                    self.on_recognition_result(text)
                    
            except sr.UnknownValueError:
                # 認識できない音声は無視（連続認識時は正常な動作）
                pass
            except sr.RequestError as e:
                if self.on_error:
                    self.on_error(f"音声認識サービスエラー: {str(e)}")
            except Exception as e:
                if self.on_error:
                    self.on_error(f"音声データ認識エラー: {str(e)}")
        
        # 別スレッドで実行
        thread = threading.Thread(target=_recognize)
        thread.daemon = True
        thread.start()
    
    def set_language(self, language_code):
        """
        認識言語を設定
        
        Args:
            language_code: 言語コード（例: 'ja-JP', 'en-US'）
        """
        self.language = language_code
    
    def test_microphone(self):
        """
        マイクロフォンのテスト
        
        Returns:
            bool: マイクが正常に動作する場合True
        """
        try:
            with self.microphone as source:
                # 短時間で環境音をテスト
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return True
        except Exception:
            return False
    
    def get_microphone_energy_threshold(self):
        """現在のマイクロフォンのエネルギー閾値を取得"""
        return self.recognizer.energy_threshold
    
    def set_microphone_energy_threshold(self, threshold):
        """
        マイクロフォンのエネルギー閾値を設定
        
        Args:
            threshold: エネルギー閾値（数値が大きいほど感度が低い）
        """
        self.recognizer.energy_threshold = threshold