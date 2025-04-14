"""
Google Agent Development Kit (ADK)を使用したYouTube字幕抽出エージェント

このモジュールはGoogle ADKを使用して、YouTubeの動画から字幕を抽出するツールを提供するエージェントを実装します。
"""
from typing import Dict, List, Any, Optional

from google.adk.agents import Agent
from .transcriptor import YouTubeTranscriptor  # 同じディレクトリ内のtranscriptorをインポート

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


# Google ADKエージェントの作成
root_agent = Agent(
    name="youtube_transcript_agent",
    model="gemini-2.0-flash-exp",
    description="YouTubeの動画から字幕を抽出し、必要に応じて翻訳するエージェント。",
    instruction="YouTube動画の字幕を抽出したり、動画URLからの字幕抽出には、言語コードの指定や翻訳機能もあります。",
    tools=[get_transcript, get_transcript_by_segments],
)
