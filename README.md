# YouTube Transcript & Search ADK

Google Agent Development Kit (ADK)を使用して、YouTube動画の検索と字幕抽出を行うツール。コマンドライン（CLI）からも利用可能です。

## 機能

- **検索機能**
  - キーワードベースでYouTube動画を検索
  - 字幕付き動画のみのフィルタリング（デフォルト）
  - 検索結果のページネーション対応
  - 並べ替えオプション（関連性、日付、評価など）

- **字幕抽出機能**
  - YouTube URLまたはビデオIDから字幕を抽出
  - 複数言語対応
  - タイムスタンプ付き字幕出力
  - 時間ごとのセグメント分割
  - JSON形式でのデータ保存

- **ADK統合**
  - Google Agent Development Kit (ADK) を使用したインテリジェントなエージェント
  - 自然言語で指示可能
  - 検索と字幕抽出の組み合わせが可能

## インストール方法

必要な依存関係をインストールします：

```bash
pip install -r requirements.txt
```

uvを使う場合：
```bash
uv venv
source .venv/bin/activate
# Windowsの場合
# .venv\Scripts\activate
uv pip install -r requirements.txt
```

## 環境設定

1. `.env`ファイルをプロジェクトルートに作成（または`.env.example`をコピー）
2. 必要なAPIキーを設定：
   ```
   # Google AI Studio のGemini APIキー
   GOOGLE_API_KEY=あなたのGemini_APIキー
   
   # YouTube Data API
   YOUTUBE_API_KEY=あなたのYouTube_APIキー
   ```
   - Gemini APIキーは [Google AI Studio](https://makersuite.google.com/app/apikey) で取得可能
   - YouTube APIキーは [Google Cloud Console](https://console.cloud.google.com/) で取得可能

## 使い方

### 検索機能（コマンドライン）

YouTube動画を検索するCLIツール：

```bash
# 基本的な使い方（対話的に検索キーワードを入力）
python test_search.py

# 検索キーワードを指定
python test_search.py --query "検索キーワード"

# 検索結果を最大10件取得
python test_search.py --query "検索キーワード" -n 10

# 並べ替え方法を指定
python test_search.py --query "検索キーワード" -o date

# 字幕フィルターを変更（デフォルトは字幕付き動画のみ）
python test_search.py --query "検索キーワード" -c any  # すべての動画
python test_search.py --query "検索キーワード" -c none  # 字幕なしの動画のみ

# 次のページを取得（前回の検索で表示されたトークンを使用）
python test_search.py --next-page "ページトークン"
```

#### 検索CLIオプション

- `--query`: 検索キーワード（指定しない場合は対話的に入力）
- `-n, --max-results`: 取得する結果の最大数（デフォルト: 5）
- `-o, --order`: 並べ替え方法（date, rating, relevance, title, viewCount）
- `-r, --region`: 地域コード（例: JP）
- `-c, --caption`: 字幕フィルター（closedCaption=字幕あり[デフォルト], none=字幕なし, any=すべて）
- `-l, --log`: 詳細なログを出力
- `--next-page`: 次のページトークンを指定して結果を取得

### 字幕抽出機能（コマンドライン）

YouTube動画から字幕を抽出するCLIツール：

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

#### 字幕CLIオプション

- `-l, --language`: 字幕の言語コード（デフォルト: ja）
- `-t, --translate`: 指定した言語が見つからない場合に翻訳する
- `-o, --output`: 出力ファイルパス
- `-s, --timestamps`: 時間情報を含める
- `--segment`: 指定した秒数ごとにセグメント化する

### Google Agent Development Kit (ADK)での実行

ADKを使用したウェブインターフェースから検索と字幕抽出の両方の機能にアクセスできます。

```bash
# プロジェクトルートディレクトリで実行
adk web
```

ブラウザで`http://localhost:8000`にアクセスし、「youtube_transcript_agent」を選択すると以下の機能が利用できます：

- `get_transcript`: YouTube動画から字幕を抽出
- `get_transcript_by_segments`: YouTube動画の字幕をセグメント単位で抽出
- `search_youtube_videos`: キーワードでYouTube動画を検索（デフォルトでは字幕付き動画のみ）

#### 使用例（エージェントへの指示）

エージェントに以下のような指示ができます：

- 「AIについての字幕付き動画を検索して」
- 「https://www.youtube.com/watch?v=VIDEO_ID の字幕を英語で取得して」
- 「VIDEO_IDの動画を30秒ごとのセグメントに分けて字幕を取得して」

## プロジェクト構造

```
youtube_transcript_adk/       # プロジェクトルート
├── youtube_transcript_adk/   # メインパッケージ
│   ├── __init__.py           # パッケージ初期化
│   ├── agent.py              # ADKエージェント定義
│   ├── transcriptor.py       # 字幕抽出機能
│   └── searcher.py           # 検索機能
├── utils/                    # ユーティリティ
│   ├── __init__.py
│   └── logger.py             # ロギング機能
├── .env.example              # 環境変数サンプル
├── test_transcript.py        # 字幕抽出CLI
├── test_search.py            # 検索CLI
└── requirements.txt          # 依存関係
```

## 注意事項

- YouTube Data APIを使用するには有効なAPIキーが必要です
- APIキーには使用量の制限があります
- 字幕抽出は字幕が利用可能な動画でのみ機能します
- デフォルトでは字幕付きの動画のみが検索されます（`-c any`オプションで変更可能）
