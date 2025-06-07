# Cloud Runへのアップロード方法
Windows環境からCloud Runにアプリケーションをビルドする際に躓いたため、備忘録として手順をまとめます。

## 忙しい人向け
- WSL環境でローカルADKの環境を構築する必要がある。
    - ==> Cloud Runにアップロードする際、パスを解釈できないような挙動がある。
- google-adkが最新バージョンじゃないとCloud Build側でエラーが発生する発生する
- .envファイルを`youtube_transcript_adk/`にコピーする
- `.set=_env.sh`を実行する
- `upload_cloud_run.sh`を実行する

## 手順
後日作成