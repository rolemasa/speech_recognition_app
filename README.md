音声文字起こしアプリケーション
日本語音声をリアルタイムでテキストに変換するデスクトップアプリケーションです。

機能
リアルタイム音声認識: 連続して話した内容を自動的にテキスト化
単発音声認識: ボタンを押してから話した内容を一回だけ認識
テキスト保存: 認識結果をテキストファイルとして保存
ファイル操作: 既存のテキストファイルを開いて編集
文字数カウント: 認識されたテキストの文字数を表示
タイムスタンプ: 各認識結果に時刻を記録
システム要件
Python 3.7 以上
Windows 10/11、macOS、または Linux
マイクロフォンデバイス
インターネット接続（Google音声認識API使用のため）
インストール手順
1. プロジェクトのダウンロード
bash
git clone <このプロジェクトのURL>
cd speech_recognition_app
2. 依存ライブラリのインストール
bash
pip install -r requirements.txt
注意: pyaudioでエラーが発生する場合は以下を試してください：

Windows の場合:

bash
pip install pipwin
pipwin install pyaudio
macOS の場合:

bash
brew install portaudio
pip install pyaudio
Linux (Ubuntu) の場合:

bash
sudo apt-get install python3-pyaudio
3. アプリケーションの起動
bash
python main.py
使用方法
基本操作
アプリケーションを起動
bash
python main.py
連続音声認識
「🎤 録音開始」ボタンをクリック
マイクに向かって話す
認識結果が自動的にテキストエリアに追加される
「⏹️ 録音停止」ボタンで停止
単発音声認識
「🎯 一回認識」ボタンをクリック
「音声待機中...」と表示されたら話す
1つの発話が認識されてテキストに追加される
テキストの保存
「💾 保存」ボタンでテキストファイルとして保存
保存場所とファイル名を指定できる
テキストファイルを開く
「📂 開く」ボタンで既存のテキストファイルを読み込み
テキストのクリア
「🗑️ クリア」ボタンでテキストエリアの内容を削除
ファイル構成
speech_recognition_app/
├── main.py                 # メインアプリケーション
├── requirements.txt        # 必要なライブラリ一覧
├── src/
│   ├── gui/
│   │   ├── main_window.py  # メインウィンドウGUI
│   │   └── styles.py       # UIスタイル設定
│   ├── audio/
│   │   ├── recorder.py     # 音声録音機能
│   │   └── recognizer.py   # 音声認識機能
│   └── utils/
│       ├── config.py       # 設定ファイル
│       └── file_handler.py # ファイル操作
├── output/                 # 保存されたテキストファイル
├── temp/                   # 一時ファイル
└── README.md              # このファイル
トラブルシューティング
よくある問題と解決方法
1. 「マイクロフォンが利用できません」エラー
原因: マイクデバイスが認識されていない、またはアクセス権限がない

解決方法:

マイクがコンピューターに正しく接続されているか確認
Windowsの場合: 設定 > プライバシー > マイク でアプリケーションのマイクアクセスを許可
macOSの場合: システム環境設定 > セキュリティとプライバシー > マイク でPythonの使用を許可
他のアプリケーションがマイクを使用していないか確認
2. 「音声認識サービスエラー」
原因: インターネット接続の問題、またはGoogle APIの制限

解決方法:

インターネット接続を確認
時間をおいて再試行
ファイアウォールやプロキシ設定を確認
3. 「pyaudio」インストールエラー
原因: システムにPortAudioライブラリがインストールされていない

解決方法:

Windows: pipwin install pyaudio
macOS: brew install portaudio 後に pip install pyaudio
Linux: sudo apt-get install python3-pyaudio
4. 音声が認識されない
原因: マイク感度、環境音、発話方法の問題

解決方法:

マイクに近づいて明瞭に話す
静かな環境で使用する
マイクの音量レベルを調整
「一回認識」で動作確認
デバッグモード
問題を特定するために、コマンドラインでアプリケーションを起動し、エラーメッセージを確認してください：

bash
python main.py
サポート
問題が解決しない場合は、以下の情報を含めてお問い合わせください：

使用OS（Windows/macOS/Linux）
Pythonバージョン（python --version）
エラーメッセージの全文
使用しているマイクデバイス
ライセンス
このプロジェクトはMITライセンスの下で公開されています。

更新履歴
v1.0.0 (2024-08-12): 初回リリース
基本的な音声認識機能
GUI実装
ファイル保存機能
リアルタイム認識機能
