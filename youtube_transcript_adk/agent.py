"""
Google Agent Development Kit (ADK)を使用したYouTube字幕抽出・検索エージェント

"""
from typing import Dict, List, Any, Optional

from google.adk.agents import Agent
from .transcriptor import YouTubeTranscriptor  # 同じディレクトリ内のtranscriptorをインポート
from .searcher import YouTubeSearch  # 検索機能をインポート

def get_transcript(url: str, language: str = "ja", translate: bool = False) -> Dict[str, Any]:
    """
    YouTubeビデオから字幕を抽出するツール
    
    Args:
        url (str): YouTube動画のURLまたはID
        language (str): 取得したい字幕の言語コード（デフォルト: "ja"）
        translate (bool): 指定言語がない場合に翻訳を試みるかどうか（デフォルト: False）
    
    Returns:
        Dict[str, Any]: ステータスと結果またはエラーメッセージを含む辞書
    """
    try:
        # YouTubeビデオIDを抽出
        video_id = YouTubeTranscriptor.extract_video_id(url)
        
        # 字幕を取得
        transcript_data = YouTubeTranscriptor.get_transcript(url, language, translate)
        
        # 最初の数行だけを表示（全文は長すぎる可能性があるため）
        sample_lines = transcript_data[:5]
        total_lines = len(transcript_data)
        
        # テキスト形式に変換
        text_content = YouTubeTranscriptor.get_transcript_text(transcript_data)
        
        # 長すぎる場合は切り詰める
        if len(text_content) > 1000:
            text_content = text_content[:1000] + "...(続きは省略)..."
        
        return {
            "status": "success",
            "video_id": video_id,
            "language": language,
            "total_lines": total_lines,
            "sample_lines": sample_lines,
            "text_content": text_content
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"字幕の取得に失敗しました: {str(e)}"
        }

def get_transcript_by_segments(url: str, language: str = "ja", segment_length: int = 30, translate: bool = False) -> Dict[str, Any]:
    """
    YouTubeビデオから字幕をセグメント化して抽出するツール
    
    Args:
        url (str): YouTube動画のURLまたはID
        language (str): 取得したい字幕の言語コード（デフォルト: "ja"）
        segment_length (int): 各セグメントの長さ（秒単位、デフォルト: 30）
        translate (bool): 指定言語がない場合に翻訳を試みるかどうか（デフォルト: False）
    
    Returns:
        Dict[str, Any]: ステータスと結果またはエラーメッセージを含む辞書
    """
    try:
        # YouTubeビデオIDを抽出
        video_id = YouTubeTranscriptor.extract_video_id(url)
        
        # セグメント化された字幕を取得
        segments = YouTubeTranscriptor.get_transcript_by_segments(url, language, segment_length, translate)
        
        # 最初の数セグメントだけを表示（全文は長すぎる可能性があるため）
        sample_segments = segments[:3]
        total_segments = len(segments)
        
        return {
            "status": "success",
            "video_id": video_id,
            "language": language,
            "segment_length": segment_length,
            "total_segments": total_segments,
            "sample_segments": sample_segments
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"セグメント化字幕の取得に失敗しました: {str(e)}"
        }


# 検索ツールを追加
def search_youtube_videos(query: str, max_results: int = 10, order: str = "relevance", 
                        caption_filter: str = "closedCaption") -> Dict[str, Any]:
    """
    YouTubeビデオを検索するツール
    
    Args:
        query (str): 検索キーワード
        max_results (int): 取得する結果の最大数（デフォルト: 10）
        order (str): 並べ替え方法（デフォルト: 'relevance'）
        caption_filter (str): 字幕フィルター（'closedCaption'=字幕あり, 'none'=字幕なし, 'any'=すべて）
    
    Returns:
        Dict[str, Any]: ステータスと検索結果を含む辞書
    """
    try:
        # YouTubeSearch クラスのインスタンス化
        youtube_search = YouTubeSearch()
        
        # 検索実行
        videos, next_page_token = youtube_search.search_videos(
            query=query,
            max_results=max_results,
            order=order,
            caption_filter=caption_filter
        )
        
        # 一部の結果のみを返す（全部は多すぎる可能性があるため）
        sample_videos = videos[:5] if len(videos) > 5 else videos
        
        return {
            "status": "success",
            "total_results": len(videos),
            "sample_videos": sample_videos,
            "has_more": next_page_token is not None
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"動画の検索に失敗しました: {str(e)}"
        }

# Google ADKエージェントの作成
root_agent = Agent(
    name="youtube_transcript_agent",
    model="gemini-2.0-flash-exp",
    description="YouTubeの動画から字幕を抽出したり、キーワードで動画を検索したりするエージェント。",
    instruction="YouTube動画の字幕抽出や検索を行います。動画URLからの字幕抽出や、キーワードでの動画検索が可能です。",
    tools=[get_transcript, get_transcript_by_segments, search_youtube_videos],
)
