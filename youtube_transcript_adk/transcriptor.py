"""
YouTubeトランスクリプト抽出モジュール
"""
import re
import json
import time
from typing import List, Dict, Optional, Union, Any
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound


class YouTubeTranscriptor:
    """YouTubeの字幕を抽出するクラス"""

    @staticmethod
    def extract_video_id(url_or_id: str) -> str:
        """
        URLまたはビデオIDからYouTubeビデオIDを抽出する
        
        Args:
            url_or_id: YouTubeのURL、または直接ビデオID
            
        Returns:
            抽出されたビデオID
            
        Raises:
            ValueError: 無効なURLまたはビデオIDの場合
        """
        # 直接ビデオIDが渡された場合（11文字の英数字-_で構成）
        if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
            return url_or_id
            
        # YouTube URLからビデオIDを抽出
        youtube_regex = (
            r'(?:https?:)?(?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtu\.be\/|youtube(?:-nocookie)?\.com\S*?[^\w\s-])'
            r'(?:watch\?v=|embed\/|v\/|shorts\/)?([a-zA-Z0-9_-]{11})'
        )
        match = re.search(youtube_regex, url_or_id, re.IGNORECASE)
        
        if match:
            return match.group(1)
        else:
            raise ValueError(f"無効なYouTube URLまたはビデオID: {url_or_id}")

    @staticmethod
    def get_transcript(url_or_id: str, language: str = 'ja', translate: bool = False) -> List[Dict[str, Any]]:
        """
        YouTubeビデオの字幕を取得する
        
        Args:
            url_or_id: YouTubeのURL、または直接ビデオID
            language: 取得したい字幕の言語コード（デフォルト: 'ja'）
            translate: 指定した言語が利用できない場合に翻訳するか（デフォルト: False）
            
        Returns:
            字幕のリスト。各項目は {'text': テキスト, 'start': 開始時間, 'duration': 表示時間} の形式
            
        Raises:
            ValueError: 無効なURLまたはビデオIDの場合
            TranscriptsDisabled: 字幕が無効になっている場合
            NoTranscriptFound: 指定した言語の字幕が見つからない場合
        """
        # ビデオIDを抽出
        video_id = YouTubeTranscriptor.extract_video_id(url_or_id)
        
        try:
            # 字幕を取得
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            if translate:
                try:
                    # まず指定された言語を検索
                    transcript_obj = transcript_list.find_transcript([language])
                    transcript = transcript_obj.fetch()
                except NoTranscriptFound:
                    # 見つからない場合は、利用可能な言語から翻訳を試みる
                    # 最初に見つかった言語を使用
                    available_transcript = next(iter(transcript_list))
                    # 指定した言語に翻訳
                    translated_transcript = available_transcript.translate(language)
                    transcript = translated_transcript.fetch()
            else:
                # 翻訳なしで指定言語のみ検索
                transcript_obj = transcript_list.find_transcript([language])
                transcript = transcript_obj.fetch()
                
            return transcript.to_raw_data()
            
        except TranscriptsDisabled:
            raise TranscriptsDisabled(f"ビデオ {video_id} では字幕が無効になっています")
        except NoTranscriptFound as e:
            # 元の例外をそのまま再スロー（引数はすでに設定されている）
            raise e

    @staticmethod
    def save_transcript_to_file(transcript: List[Dict[str, Any]], output_path: str) -> None:
        """
        取得した字幕をファイルに保存する
        
        Args:
            transcript: 字幕データ
            output_path: 保存先のファイルパス
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_transcript_text(transcript: List[Dict[str, Any]], include_timestamps: bool = False) -> str:
        """
        字幕からテキストのみを抽出する
        
        Args:
            transcript: 字幕データ
            include_timestamps: 時間情報を含めるかどうか
            
        Returns:
            抽出されたテキスト（時間情報付きまたはなし）
        """
        if include_timestamps:
            # 時間情報付きのテキスト
            result = []
            for item in transcript:
                timestamp = time.strftime('%H:%M:%S', time.gmtime(item['start']))
                result.append(f"[{timestamp}] {item['text']}")
            return '\n'.join(result)
        else:
            # テキストのみ
            return ' '.join(item['text'] for item in transcript)

    @staticmethod
    def get_transcript_by_segments(url_or_id: str, language: str = 'ja', segment_length: int = 5, translate: bool = False) -> List[Dict[str, Any]]:
        """
        字幕を時間ごとのセグメントに分割する
        
        Args:
            url_or_id: YouTubeのURL、または直接ビデオID
            language: 取得したい字幕の言語コード（デフォルト: 'ja'）
            segment_length: 1セグメントの時間（秒）
            translate: 指定した言語が利用できない場合に翻訳するか（デフォルト: False）
            
        Returns:
            セグメント化された字幕のリスト
        """
        transcript = YouTubeTranscriptor.get_transcript(url_or_id, language, translate)
        
        segments = []
        current_segment = {"start": 0, "text": "", "end": segment_length}
        
        for item in transcript:
            item_start = item['start']
            item_end = item_start + item['duration']
            
            # 現在のセグメントに含まれるか確認
            if item_start < current_segment["end"]:
                current_segment["text"] += " " + item['text']
            else:
                # 新しいセグメントを開始
                if current_segment["text"]:
                    segments.append(current_segment)
                
                # 次のセグメント範囲を計算
                segment_start = (item_start // segment_length) * segment_length
                current_segment = {
                    "start": segment_start,
                    "text": item['text'],
                    "end": segment_start + segment_length
                }
        
        # 最後のセグメントを追加
        if current_segment["text"]:
            segments.append(current_segment)
            
        return segments
