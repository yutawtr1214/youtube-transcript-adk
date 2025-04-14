# YouTube Transcript Extractor

YouTubeビデオから字幕（トランスクリプト）を抽出するPythonモジュール。

## 機能

- YouTube URLまたはビデオIDから字幕を抽出
- 複数言語対応
- タイムスタンプ付き字幕出力
- 時間ごとのセグメント分割
- JSON形式でのデータ保存
- ADK (Agent Development Kit) インテグレーション

## インストール方法

必要な依存関係をインストールします：

```bash
pip install -r requirements.txt
```
uvを使う場合
```bash
uv venv
source .venv/bin/activvate
.venv\Scripts\activate //windows
uv pip install -r requirements.txt
```

## 使い方

### Google Agent Development Kit (ADK)による実行

Google Agent Development Kit (ADK)を通じてウェブインターフェースから利用することができます。

#### セットアップ

1. 環境変数の設定:
   - `.env`ファイルを作成（またはサンプルからコピー）し、`GOOGLE_API_KEY`にGemini APIキーを設定してください
   - Google AI Studio（https://makersuite.google.com/app/apikey）でAPIキーを取得できます


#### 実行

```bash
# プロジェクトルートディレクトリで以下を実行
adk web
```

ブラウザで`http://localhost:8000`にアクセスし、「youtube_transcript_agent」を選択すると、以下の機能が利用できます：

- `get_transcript`: YouTube動画から字幕を抽出
- `get_transcript_by_segments`: YouTube動画の字幕をセグメント単位で抽出

#### 使用例

エージェントに以下のような質問ができます：

- 「https://www.youtube.com/watch?v=VIDEO_ID の字幕を英語で取得して」
- 「VIDEO_IDの動画を30秒ごとのセグメントに分けて字幕を取得して」

### コマンドラインから（機能テスト用）

基本機能をコマンドラインから簡単にテストすることもできます：

```bash
# 基本的な使い方
python test_transcript.py https://www.youtube.com/watch?v=VIDEO_ID

# 英語の字幕を取得
python test_transcript.py https://www.youtube.com/watch?v=VIDEO_ID -l en

# タイムスタンプ付きで出力
python test_transcript.py https://www.youtube.com/watch?v=VIDEO_ID -s

# ファイルに保存
python test_transcript.py https://www.youtube.com/watch?v=VIDEO_ID -o output.json

# 5秒ごとにセグメント化
python test_transcript.py https://www.youtube.com/watch?v=VIDEO_ID --segment 5

# 自動翻訳を使用
python test_transcript.py https://www.youtube.com/watch?v=VIDEO_ID -t
```

#### コマンドラインオプション

- `-l, --language`: 字幕の言語コード（デフォルト: ja）
- `-t, --translate`: 指定した言語が見つからない場合に翻訳する
- `-o, --output`: 出力ファイルパス
- `-s, --timestamps`: 時間情報を含める
- `--segment`: 指定した秒数ごとにセグメント化する（このオプションを指定すると自動的にタイムスタンプも有効になります）

### プログラムから

コア機能を他のPythonプログラムから利用することもできます：

```python
from adk.transcriptor import YouTubeTranscriptor

# 字幕を取得
transcript = YouTubeTranscriptor.get_transcript('https://www.youtube.com/watch?v=VIDEO_ID', language='ja')

# テキストのみを抽出
text = YouTubeTranscriptor.get_transcript_text(transcript)
print(text)

# タイムスタンプ付きテキストを取得
text_with_timestamps = YouTubeTranscriptor.get_transcript_text(transcript, include_timestamps=True)
print(text_with_timestamps)

# ファイルに保存
YouTubeTranscriptor.save_transcript_to_file(transcript, 'output.json')

# セグメント化
segments = YouTubeTranscriptor.get_transcript_by_segments('https://www.youtube.com/watch?v=VIDEO_ID', segment_length=5)
```

## プロジェクト構造

```
youtube_transcript_adk/       # プロジェクトルート
├── adk/                     # ADK インテグレーション用
│   ├── __init__.py          # ADKパッケージ初期化
│   ├── agent.py             # ADKエージェント定義
│   └── transcriptor.py      # コア機能モジュール
├── .env.example             # パッケージ初期化
├── test_transcript.py       # CLIインターフェース
└── requirements.txt         # 依存関係
```
