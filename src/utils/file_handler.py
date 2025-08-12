# -*- coding: utf-8 -*-
"""
ファイル操作を管理するモジュール
"""

import os
from datetime import datetime
from tkinter import filedialog, messagebox
from .config import Config

class FileHandler:
    """ファイル操作を管理するクラス"""
    
    @staticmethod
    def save_text_as_file(text_content, parent_window=None):
        """
        テキストをファイルに保存
        
        Args:
            text_content (str): 保存するテキスト内容
            parent_window: 親ウィンドウ（ダイアログの親）
            
        Returns:
            bool: 保存成功の場合True
        """
        if not text_content.strip():
            messagebox.showwarning("警告", "保存するテキストがありません。")
            return False
        
        # デフォルトファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"音声認識結果_{timestamp}.txt"
        
        try:
            # ファイル保存ダイアログを表示
            file_path = filedialog.asksaveasfilename(
                parent=parent_window,
                title="テキストファイルを保存",
                defaultextension=Config.DEFAULT_SAVE_FORMAT,
                initialdir=Config.OUTPUT_DIR,
                initialfile=default_filename,
                filetypes=Config.SUPPORTED_FORMATS
            )
            
            if file_path:
                # ファイルに書き込み
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text_content)
                
                messagebox.showinfo("完了", f"ファイルを保存しました:\n{file_path}")
                return True
            
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの保存に失敗しました:\n{str(e)}")
        
        return False
    
    @staticmethod
    def auto_save_text(text_content, prefix="auto_save"):
        """
        テキストを自動保存
        
        Args:
            text_content (str): 保存するテキスト内容
            prefix (str): ファイル名のプレフィックス
            
        Returns:
            str: 保存されたファイルのパス（失敗時はNone）
        """
        if not text_content.strip():
            return None
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prefix}_{timestamp}.txt"
            file_path = os.path.join(Config.OUTPUT_DIR, filename)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_content)
            
            return file_path
            
        except Exception as e:
            print(f"自動保存エラー: {e}")
            return None
    
    @staticmethod
    def load_text_from_file(parent_window=None):
        """
        テキストファイルを読み込み
        
        Args:
            parent_window: 親ウィンドウ
            
        Returns:
            str: ファイルの内容（失敗時は空文字）
        """
        try:
            file_path = filedialog.askopenfilename(
                parent=parent_window,
                title="テキストファイルを開く",
                initialdir=Config.OUTPUT_DIR,
                filetypes=Config.SUPPORTED_FORMATS
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            
        except Exception as e:
            messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました:\n{str(e)}")
        
        return ""
    
    @staticmethod
    def get_output_files_list():
        """
        出力ディレクトリ内のファイル一覧を取得
        
        Returns:
            list: ファイルパスのリスト
        """
        try:
            if not os.path.exists(Config.OUTPUT_DIR):
                return []
            
            files = []
            for filename in os.listdir(Config.OUTPUT_DIR):
                if filename.endswith('.txt'):
                    file_path = os.path.join(Config.OUTPUT_DIR, filename)
                    files.append(file_path)
            
            return sorted(files, key=os.path.getmtime, reverse=True)  # 更新日時順
            
        except Exception as e:
            print(f"ファイル一覧取得エラー: {e}")
            return []
    
    @staticmethod
    def cleanup_temp_files():
        """一時ファイルをクリーンアップ"""
        try:
            if os.path.exists(Config.TEMP_DIR):
                for filename in os.listdir(Config.TEMP_DIR):
                    file_path = os.path.join(Config.TEMP_DIR, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        except Exception as e:
            print(f"一時ファイル削除エラー: {e}")