"""
YouTube Data APIを使用した検索機能モジュール
"""
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

class YouTubeSearch:
    """
    YouTube Data API を使用して検索を行うクラス
    """
    
    def __init__(self, api_key=None, logger=None):
        """
        初期化関数
        
        Args:
            api_key: YouTube API キー（Noneの場合は環境変数から取得）
            logger: ロガーインスタンス
        """
        if api_key is None:
            # .env ファイルから API キーを読み込む
            load_dotenv()
            api_key = os.getenv('YOUTUBE_API_KEY')
            
            if not api_key:
                raise ValueError("API キーが指定されていません。.env ファイルを確認してください。")
        
        self.api_key = api_key
        self.logger = logger
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_videos(self, query, max_results=10, order='relevance', video_type=None, 
                     published_after=None, published_before=None, region_code=None,
                     caption_filter='closedCaption'):  # デフォルトで字幕付き動画のみを検索
        """
        キーワードに基づいて動画を検索する
        
        Args:
            query: 検索キーワード
            max_results: 取得する結果の最大数（最大50件）
            order: 並べ替え方法（'date', 'rating', 'relevance', 'title', 'viewCount'）
            video_type: 動画タイプ（'any', 'movie', 'episode'）
            published_after: この日時以降に公開された動画のみを検索（ISO 8601形式）
            published_before: この日時以前に公開された動画のみを検索（ISO 8601形式）
            region_code: 特定の地域のコンテンツを優先（ISO 3166-1 alpha-2国コード）
            caption_filter: 字幕フィルター（'closedCaption'=字幕あり, 'none'=字幕なし, 'any'=すべて）
            
        Returns:
            (videos, next_page_token) のタプル
            videos: 検索結果の辞書リスト
            next_page_token: 次のページを取得するためのトークン（次のページがない場合はNone）
        """
        try:
            # 検索リクエストを作成（パラメータを全て一度に指定）
            request_params = {
                'part': 'id,snippet',
                'q': query,
                'maxResults': max_results,
                'order': order,
                'type': 'video'  # 動画のみを検索
            }
            
            # 字幕フィルターの指定（デフォルトで字幕付き動画のみ）
            if caption_filter in ['closedCaption', 'none', 'any']:
                request_params['videoCaption'] = caption_filter
            
            # その他のオプションパラメータの追加
            if video_type:
                request_params['videoType'] = video_type
            if published_after:
                request_params['publishedAfter'] = published_after
            if published_before:
                request_params['publishedBefore'] = published_before
            if region_code:
                request_params['regionCode'] = region_code
                
            # リクエストを実行
            request = self.youtube.search().list(**request_params)
            response = request.execute()
            
            # 次のページトークンを取得（存在しない場合はNone）
            next_page_token = response.get('nextPageToken', None)
            
            if self.logger:
                self.logger.info(f"検索キーワード '{query}' で {len(response.get('items', []))} 件の動画が見つかりました")
                if next_page_token:
                    self.logger.info("次のページが利用可能です")
            
            # 検索結果から必要な情報を抽出
            videos = []
            for item in response.get('items', []):
                video_info = {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
                    'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video_info)
                
                if self.logger:
                    self.logger.info(f"動画: {video_info['title']} (ID: {video_info['id']})")
            
            return videos, next_page_token
            
        except HttpError as e:
            error_message = f"YouTube API エラー: {e}"
            if self.logger:
                self.logger.error(error_message)
            raise Exception(error_message)
            
    def get_next_page(self, query, next_page_token, max_results=10, order='relevance', video_type=None,
                     published_after=None, published_before=None, region_code=None,
                     caption_filter='closedCaption'):  # デフォルトで字幕付き動画のみを検索
        """
        検索結果の次のページを取得する
        
        Args:
            query: 検索キーワード
            next_page_token: 次のページを取得するためのトークン
            max_results: 取得する結果の最大数（最大50件）
            order: 並べ替え方法（'date', 'rating', 'relevance', 'title', 'viewCount'）
            video_type: 動画タイプ（'any', 'movie', 'episode'）
            published_after: この日時以降に公開された動画のみを検索（ISO 8601形式）
            published_before: この日時以前に公開された動画のみを検索（ISO 8601形式）
            region_code: 特定の地域のコンテンツを優先（ISO 3166-1 alpha-2国コード）
            caption_filter: 字幕フィルター（'closedCaption'=字幕あり, 'none'=字幕なし, 'any'=すべて）
            
        Returns:
            検索結果の辞書リストと次のページトークン
        """
        try:
            # 検索リクエストを作成（パラメータを全て一度に指定）
            request_params = {
                'part': 'id,snippet',
                'q': query,
                'maxResults': max_results,
                'order': order,
                'type': 'video',  # 動画のみを検索
                'pageToken': next_page_token
            }
            
            # 字幕フィルターの指定（デフォルトで字幕付き動画のみ）
            if caption_filter in ['closedCaption', 'none', 'any']:
                request_params['videoCaption'] = caption_filter
            
            # その他のオプションパラメータの追加
            if video_type:
                request_params['videoType'] = video_type
            if published_after:
                request_params['publishedAfter'] = published_after
            if published_before:
                request_params['publishedBefore'] = published_before
            if region_code:
                request_params['regionCode'] = region_code
                
            # リクエストを実行
            request = self.youtube.search().list(**request_params)
            response = request.execute()
            
            # 次のページトークンを取得（存在しない場合はNone）
            next_page_token = response.get('nextPageToken', None)
            
            if self.logger:
                self.logger.info(f"検索キーワード '{query}' の次のページで {len(response.get('items', []))} 件の動画が見つかりました")
            
            # 検索結果から必要な情報を抽出
            videos = []
            for item in response.get('items', []):
                video_info = {
                    'id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt'],
                    'channel_id': item['snippet']['channelId'],
                    'channel_title': item['snippet']['channelTitle'],
                    'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
                    'video_url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                }
                videos.append(video_info)
                
                if self.logger:
                    self.logger.info(f"動画: {video_info['title']} (ID: {video_info['id']})")
            
            return videos, next_page_token
            
        except HttpError as e:
            error_message = f"YouTube API エラー: {e}"
            if self.logger:
                self.logger.error(error_message)
            raise Exception(error_message)
