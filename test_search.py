#!/usr/bin/env python3
"""
YouTube検索モジュールのテストスクリプト
"""
import os
import sys
import argparse
from dotenv import load_dotenv
from youtube_transcript_adk.searcher import YouTubeSearch
from utils.logger import setup_logger

def main():
    """メイン実行関数"""
    # 環境変数の読み込み
    load_dotenv()
    
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='YouTubeビデオを検索するプログラム')
    parser.add_argument('-n', '--max-results', type=int, default=5, 
                      help='取得する結果の最大数（デフォルト: 5）')
    parser.add_argument('-o', '--order', default='relevance', 
                      choices=['date', 'rating', 'relevance', 'title', 'viewCount'],
                      help='結果の並べ替え方法（デフォルト: relevance）')
    parser.add_argument('-r', '--region', help='地域コード（例: JP）')
    parser.add_argument('-l', '--log', action='store_true', 
                      help='詳細なログを出力する')
    parser.add_argument('-c', '--caption', default='closedCaption',
                      choices=['closedCaption', 'none', 'any'],
                      help='字幕フィルター（closedCaption=字幕あり(デフォルト), none=字幕なし, any=すべて）')
    parser.add_argument('--next-page', metavar='TOKEN', 
                      help='次のページトークンを指定して結果を取得する')
    parser.add_argument('--query', help='検索キーワード（指定しない場合は対話的に入力）')
    
    args = parser.parse_args()
    
    try:
        # ロガーの設定（オプション）
        logger = setup_logger('youtube_search') if args.log else None
        
        # YouTube API キーの取得
        api_key = os.getenv('YOUTUBE_API_KEY')
        if not api_key:
            print("警告: YOUTUBE_API_KEYが設定されていません。.envファイルを確認してください。", file=sys.stderr)
            return 1
        
        # YouTube 検索クラスのインスタンス化
        youtube_search = YouTubeSearch(api_key=api_key, logger=logger)
        
        # クエリを取得（引数で指定されていない場合は入力を求める）
        query = args.query
        next_page_token = args.next_page
        
        # 次のページトークンが指定されている場合
        if next_page_token:
            if not query:
                query = input("検索キーワードを入力してください: ")
                
            # 次のページを取得
            videos, next_page_token = youtube_search.get_next_page(
                query=query,
                next_page_token=next_page_token,
                max_results=args.max_results,
                order=args.order,
                region_code=args.region,
                caption_filter=args.caption
            )
            print(f"\n次のページの検索結果: {len(videos)} 件の動画が見つかりました\n")
        else:
            # 通常の検索の場合
            if not query:
                query = input("検索キーワードを入力してください: ")
                
            # 検索を実行
            videos, next_page_token = youtube_search.search_videos(
                query=query,
                max_results=args.max_results,
                order=args.order,
                region_code=args.region,
                caption_filter=args.caption
            )
            print(f"\n検索結果: {len(videos)} 件の動画が見つかりました\n")
        
        # 結果表示
        for i, video in enumerate(videos, 1):
            print(f"=== 動画 {i} ===")
            print(f"タイトル: {video['title']}")
            print(f"チャンネル: {video['channel_title']}")
            print(f"URL: {video['video_url']}")
            print(f"公開日時: {video['published_at']}")
            print(f"説明: {video['description'][:100]}..." if len(video['description']) > 100 else f"説明: {video['description']}")
            print()
        
        # 次のページ取得オプション
        if next_page_token:
            print(f"注: さらに結果があります。次のページを取得するには:")
            print(f"    python {sys.argv[0]} --query \"{query}\" --next-page {next_page_token} -c {args.caption}")
            print(f"    または")
            print(f"    python {sys.argv[0]} --next-page {next_page_token} -c {args.caption}")
        
        return 0
        
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
