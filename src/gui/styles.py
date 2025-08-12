# -*- coding: utf-8 -*-
"""
GUI スタイル定義モジュール
"""

from ..utils.config import Config

class AppStyles:
    """アプリケーションのスタイル定義クラス"""
    
    # フォント定義
    FONTS = {
        'title': ('Arial', 18, 'bold'),
        'heading': ('Arial', 14, 'bold'),
        'button': ('Arial', 11, 'bold'),
        'label': ('Arial', 10),
        'text': ('Arial', 11),
        'status': ('Arial', 9)
    }
    
    # ボタンスタイル
    BUTTON_STYLES = {
        'primary': {
            'bg': Config.COLORS['primary'],
            'fg': 'white',
            'font': FONTS['button'],
            'relief': 'raised',
            'bd': 2,
            'padx': 20,
            'pady': 5
        },
        'success': {
            'bg': Config.COLORS['success'],
            'fg': 'white',
            'font': FONTS['button'],
            'relief': 'raised',
            'bd': 2,
            'padx': 20,
            'pady': 5
        },
        'danger': {
            'bg': Config.COLORS['danger'],
            'fg': 'white',
            'font': FONTS['button'],
            'relief': 'raised',
            'bd': 2,
            'padx': 20,
            'pady': 5
        },
        'warning': {
            'bg': Config.COLORS['warning'],
            'fg': 'white',
            'font': FONTS['button'],
            'relief': 'raised',
            'bd': 2,
            'padx': 15,
            'pady': 5
        },
        'info': {
            'bg': Config.COLORS['info'],
            'fg': 'white',
            'font': FONTS['button'],
            'relief': 'raised',
            'bd': 2,
            'padx': 15,
            'pady': 5
        }
    }
    
    # ラベルスタイル
    LABEL_STYLES = {
        'title': {
            'font': FONTS['title'],
            'fg': Config.COLORS['dark'],
            'pady': 10
        },
        'heading': {
            'font': FONTS['heading'],
            'fg': Config.COLORS['dark'],
            'pady': 5
        },
        'normal': {
            'font': FONTS['label'],
            'fg': Config.COLORS['dark']
        },
        'status_ready': {
            'font': FONTS['status'],
            'fg': Config.COLORS['success']
        },
        'status_recording': {
            'font': FONTS['status'],
            'fg': Config.COLORS['danger']
        },
        'status_processing': {
            'font': FONTS['status'],
            'fg': Config.COLORS['warning']
        },
        'status_error': {
            'font': FONTS['status'],
            'fg': Config.COLORS['danger']
        }
    }
    
    # フレームスタイル
    FRAME_STYLES = {
        'main': {
            'bg': Config.COLORS['light'],
            'relief': 'flat',
            'bd': 0
        },
        'control': {
            'bg': Config.COLORS['light'],
            'relief': 'raised',
            'bd': 1,
            'padx': 10,
            'pady': 10
        },
        'text_area': {
            'bg': 'white',
            'relief': 'sunken',
            'bd': 2,
            'padx': 5,
            'pady': 5
        }
    }
    
    # テキストエリアスタイル
    TEXT_AREA_STYLE = {
        'font': FONTS['text'],
        'bg': 'white',
        'fg': Config.COLORS['dark'],
        'wrap': 'word',
        'relief': 'sunken',
        'bd': 2,
        'padx': 10,
        'pady': 10,
        'insertbackground': Config.COLORS['primary']  # カーソル色
    }
    
    # エントリー（入力欄）スタイル
    ENTRY_STYLE = {
        'font': FONTS['text'],
        'bg': 'white',
        'fg': Config.COLORS['dark'],
        'relief': 'sunken',
        'bd': 2,
        'insertbackground': Config.COLORS['primary']
    }
    
    # メニューバースタイル
    MENUBAR_STYLE = {
        'bg': Config.COLORS['light'],
        'fg': Config.COLORS['dark'],
        'font': FONTS['label']
    }
    
    # ツールチップスタイル
    TOOLTIP_STYLE = {
        'bg': Config.COLORS['info'],
        'fg': 'white',
        'font': FONTS['status'],
        'relief': 'solid',
        'bd': 1
    }