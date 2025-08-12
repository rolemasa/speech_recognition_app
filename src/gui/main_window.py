# -*- coding: utf-8 -*-
"""
メインウィンドウのGUIを管理するモジュール
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import time
from datetime import datetime

from ..utils.config import Config
from ..utils.file_handler import FileHandler
from ..audio.recorder import AudioRecorder
from ..audio.recognizer import SpeechRecognizer
from .styles import AppStyles

class MainWindow:
    """メインウィンドウクラス"""
    
    def __init__(self):
        # メインウィンドウの作成
        self.root = tk.Tk()
        self.root.title(Config.APP_NAME)
        self.root.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")
        self.root.minsize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)
        
        # ファイルハンドラー
        self.file_handler = FileHandler()
        
        # 音声録音・認識の初期化
        self.audio_recorder = AudioRecorder()
        self.speech_recognizer = SpeechRecognizer()
        
        # 状態変数
        self.is_recording = False
        self.start_time = None
        
        # コールバック設定
        self._setup_callbacks()
        
        # UI構築
        self._setup_ui()
        
        # ディレクトリ作成
        Config.ensure_directories()
        
        # 終了時の処理を設定
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_callbacks(self):
        """音声処理のコールバック関数を設定"""
        # 録音コールバック
        self.audio_recorder.set_callbacks(
            on_audio_data=self._on_audio_data,
            on_error=self._on_audio_error
        )
        
        # 認識コールバック
        self.speech_recognizer.set_callbacks(
            on_recognition_result=self._on_recognition_result,
            on_error=self._on_recognition_error,
            on_listening=self._on_listening_start
        )
    
    def _setup_ui(self):
        """UIコンポーネントを構築"""
        # メインフレーム
        main_frame = tk.Frame(self.root, **AppStyles.FRAME_STYLES['main'])
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # タイトル
        title_label = tk.Label(main_frame, text=Config.APP_NAME, **AppStyles.LABEL_STYLES['title'])
        title_label.pack()
        
        # コントロールフレーム
        self._create_control_frame(main_frame)
        
        # ステータスフレーム
        self._create_status_frame(main_frame)
        
        # テキストエリアフレーム
        self._create_text_area_frame(main_frame)
        
        # 情報フレーム
        self._create_info_frame(main_frame)
    
    def _create_control_frame(self, parent):
        """コントロール部分のUI作成"""
        control_frame = tk.Frame(parent, **AppStyles.FRAME_STYLES['control'])
        control_frame.pack(fill="x", pady=(10, 0))
        
        # 録音ボタン
        self.record_button = tk.Button(
            control_frame,
            text="🎤 録音開始",
            command=self._toggle_recording,
            **AppStyles.BUTTON_STYLES['success']
        )
        self.record_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # 一回だけ認識ボタン
        once_button = tk.Button(
            control_frame,
            text="🎯 一回認識",
            command=self._recognize_once,
            **AppStyles.BUTTON_STYLES['primary']
        )
        once_button.pack(side=tk.LEFT, padx=5)
        
        # 区切り線
        separator = ttk.Separator(control_frame, orient='vertical')
        separator.pack(side=tk.LEFT, fill='y', padx=10)
        
        # ファイル操作ボタン群
        file_frame = tk.Frame(control_frame, bg=control_frame['bg'])
        file_frame.pack(side=tk.LEFT, padx=10)
        
        # 開くボタン
        open_button = tk.Button(
            file_frame,
            text="📂 開く",
            command=self._open_file,
            **AppStyles.BUTTON_STYLES['info']
        )
        open_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # 保存ボタン
        save_button = tk.Button(
            file_frame,
            text="💾 保存",
            command=self._save_file,
            **AppStyles.BUTTON_STYLES['info']
        )
        save_button.pack(side=tk.LEFT, padx=5)
        
        # クリアボタン
        clear_button = tk.Button(
            control_frame,
            text="🗑️ クリア",
            command=self._clear_text,
            **AppStyles.BUTTON_STYLES['warning']
        )
        clear_button.pack(side=tk.RIGHT)
    
    def _create_status_frame(self, parent):
        """ステータス表示部分のUI作成"""
        status_frame = tk.Frame(parent, bg=parent['bg'])
        status_frame.pack(fill="x", pady=10)
        
        # ステータスラベル
        self.status_label = tk.Label(
            status_frame,
            text="🟢 準備完了",
            **AppStyles.LABEL_STYLES['status_ready']
        )
        self.status_label.pack(side=tk.LEFT)
        
        # 録音時間ラベル
        self.time_label = tk.Label(
            status_frame,
            text="⏱️ 00:00",
            **AppStyles.LABEL_STYLES['normal']
        )
        self.time_label.pack(side=tk.RIGHT)
    
    def _create_text_area_frame(self, parent):
        """テキスト表示エリアのUI作成"""
        text_frame = tk.LabelFrame(
            parent,
            text="📝 認識結果",
            font=AppStyles.FONTS['heading'],
            fg=Config.COLORS['dark']
        )
        text_frame.pack(expand=True, fill="both", pady=(10, 0))
        
        # テキストエリア
        self.text_area = scrolledtext.ScrolledText(
            text_frame,
            **AppStyles.TEXT_AREA_STYLE
        )
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)
        
        # プレースホルダーテキスト
        placeholder_text = (
            "音声認識結果がここに表示されます。\n\n"
            "使い方:\n"
            "• 「録音開始」ボタンで連続録音・認識\n"
            "• 「一回認識」ボタンで単発の音声認識\n"
            "• 認識結果は自動的にここに追加されます\n"
            "• 「保存」ボタンでテキストファイルとして保存できます"
        )
        self.text_area.insert("1.0", placeholder_text)
        self.text_area.config(fg=Config.COLORS['secondary'])
    
    def _create_info_frame(self, parent):
        """情報表示部分のUI作成"""
        info_frame = tk.Frame(parent, bg=parent['bg'])
        info_frame.pack(fill="x", pady=(10, 0))
        
        # 文字数表示
        self.char_count_label = tk.Label(
            info_frame,
            text="📊 文字数: 0",
            **AppStyles.LABEL_STYLES['normal']
        )
        self.char_count_label.pack(side=tk.LEFT)
        
        # バージョン表示
        version_label = tk.Label(
            info_frame,
            text=f"v{Config.APP_VERSION}",
            **AppStyles.LABEL_STYLES['normal']
        )
        version_label.pack(side=tk.RIGHT)
    
    def _toggle_recording(self):
        """録音の開始/停止を切り替え"""
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()
    
    def _start_recording(self):
        """録音開始"""
        if not self.audio_recorder.is_microphone_available():
            messagebox.showerror("エラー", "マイクロフォンが利用できません。")
            return
        
        if self.audio_recorder.start_recording():
            self.is_recording = True
            self.start_time = time.time()
            
            # UI更新
            self.record_button.config(
                text="⏹️ 録音停止",
                **AppStyles.BUTTON_STYLES['danger']
            )
            self.status_label.config(
                text="🔴 録音中...",
                **AppStyles.LABEL_STYLES['status_recording']
            )
            
            # プレースホルダーテキストをクリア
            self._clear_placeholder_text()
            
            # 時間更新を開始
            self._update_recording_time()
    
    def _stop_recording(self):
        """録音停止"""
        self.audio_recorder.stop_recording()
        self.is_recording = False
        
        # UI更新
        self.record_button.config(
            text="🎤 録音開始",
            **AppStyles.BUTTON_STYLES['success']
        )
        self.status_label.config(
            text="🟢 準備完了",
            **AppStyles.LABEL_STYLES['status_ready']
        )
    
    def _recognize_once(self):
        """一回だけ音声認識を実行"""
        if not self.speech_recognizer.test_microphone():
            messagebox.showerror("エラー", "マイクロフォンが利用できません。")
            return
        
        self._clear_placeholder_text()
        self.speech_recognizer.recognize_from_microphone_once()
    
    def _update_recording_time(self):
        """録音時間を更新"""
        if self.is_recording and self.start_time:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.time_label.config(text=f"⏱️ {minutes:02d}:{seconds:02d}")
            
            # 1秒後に再実行
            self.root.after(1000, self._update_recording_time)
        else:
            self.time_label.config(text="⏱️ 00:00")
    
    def _clear_placeholder_text(self):
        """プレースホルダーテキストをクリア"""
        current_text = self.text_area.get("1.0", tk.END).strip()
        if "音声認識結果がここに表示されます" in current_text:
            self.text_area.delete("1.0", tk.END)
            self.text_area.config(fg=Config.COLORS['dark'])
    
    def _add_recognized_text(self, text):
        """認識されたテキストを追加"""
        if text.strip():
            # タイムスタンプ付きで追加
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            current_text = self.text_area.get("1.0", tk.END).strip()
            if current_text:
                self.text_area.insert(tk.END, f"\n[{timestamp}] {text}")
            else:
                self.text_area.insert(tk.END, f"[{timestamp}] {text}")
            
            # 自動スクロール
            self.text_area.see(tk.END)
            
            # 文字数更新
            self._update_char_count()
    
    def _update_char_count(self):
        """文字数を更新"""
        text_content = self.text_area.get("1.0", tk.END).strip()
        char_count = len(text_content)
        self.char_count_label.config(text=f"📊 文字数: {char_count}")
    
    def _clear_text(self):
        """テキストエリアをクリア"""
        if messagebox.askyesno("確認", "テキストをクリアしますか？"):
            self.text_area.delete("1.0", tk.END)
            self._update_char_count()
    
    def _open_file(self):
        """ファイルを開く"""
        text_content = self.file_handler.load_text_from_file(self.root)
        if text_content:
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", text_content)
            self.text_area.config(fg=Config.COLORS['dark'])
            self._update_char_count()
    
    def _save_file(self):
        """ファイルに保存"""
        text_content = self.text_area.get("1.0", tk.END).strip()
        self.file_handler.save_text_as_file(text_content, self.root)
    
    # コールバック関数
    def _on_audio_data(self, audio_data):
        """音声データ受信時の処理"""
        self.speech_recognizer.recognize_from_audio_data(audio_data)
    
    def _on_audio_error(self, error_message):
        """音声録音エラー時の処理"""
        self.root.after(0, lambda: self._show_error(error_message))
    
    def _on_recognition_result(self, text):
        """音声認識結果受信時の処理"""
        self.root.after(0, lambda: self._add_recognized_text(text))
    
    def _on_recognition_error(self, error_message):
        """音声認識エラー時の処理"""
        self.root.after(0, lambda: self._show_error(error_message))
    
    def _on_listening_start(self):
        """音声待機開始時の処理"""
        self.root.after(0, lambda: self.status_label.config(
            text="👂 音声待機中...",
            **AppStyles.LABEL_STYLES['status_processing']
        ))
    
    def _show_error(self, error_message):
        """エラーメッセージを表示"""
        self.status_label.config(
            text=f"❌ エラー: {error_message}",
            **AppStyles.LABEL_STYLES['status_error']
        )
        # 5秒後に元に戻す
        self.root.after(5000, lambda: self.status_label.config(
            text="🟢 準備完了",
            **AppStyles.LABEL_STYLES['status_ready']
        ))
    
    def _on_closing(self):
        """アプリケーション終了時の処理"""
        if self.is_recording:
            self._stop_recording()
        
        # リソースのクリーンアップ
        self.audio_recorder.cleanup()
        self.file_handler.cleanup_temp_files()
        
        # ウィンドウを閉じる
        self.root.destroy()
    
    def run(self):
        """アプリケーションを実行"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("アプリケーションを終了します。")
        except Exception as e:
            messagebox.showerror("致命的エラー", f"アプリケーションエラー: {str(e)}")
        finally:
            self._on_closing()