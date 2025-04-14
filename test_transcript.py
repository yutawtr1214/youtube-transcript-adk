#!/usr/bin/env python3
"""
YouTubeトランスクリプト抽出モジュールのテストスクリプト
"""
import os
import sys
import argparse
from youtube_transcript_adk.transcriptor import YouTubeTranscriptor
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound


def main():
    """メイン実行関数"""
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='YouTubeビデオの字幕を抽出するプログラム')
    parser.add_argument('url', help='YouTubeビデオのURLまたはID')
    parser.add_argument('-l', '--language', default='ja', help='字幕の言語コード（デフォルト: ja）')
    parser.add_argument('-t', '--translate', action='store_true', 
                        help='指定した言語が見つからない場合に翻訳する')
    parser.add_argument('-o', '--output', help='出力ファイルパス（指定しない場合は標準出力に表示）')
    parser.add_argument('-s', '--timestamps', action='store_true', help='時間情報を含める')
    parser.add_argument('--segment', type=int, default=0, 
                        help='指定した秒数ごとにセグメント化する（デフォルト: 0 = セグメント化しない）')

    args = parser.parse_args()
    
    # セグメント化が指定された場合は自動的にタイムスタンプを有効にする
    if args.segment > 0 and not args.timestamps:
        args.timestamps = True
        print("注意: セグメント化が指定されたため、タイムスタンプ表示を自動的に有効にしました")

    try:
        # ビデオIDの抽出を試みる
        video_id = YouTubeTranscriptor.extract_video_id(args.url)
        print(f"処理中のビデオID: {video_id}")

        # セグメント化するかどうかで処理を分岐
        if args.segment > 0:
            transcript_data = YouTubeTranscriptor.get_transcript_by_segments(
                args.url, args.language, args.segment, args.translate
            )
            print(f"{len(transcript_data)}個のセグメントに分割しました")
        else:
            # 通常の字幕取得
            transcript_data = YouTubeTranscriptor.get_transcript(
                args.url, args.language, args.translate
            )
            print(f"{len(transcript_data)}個の字幕を取得しました")

        # 出力処理
        if args.output:
            # ファイルに保存
            YouTubeTranscriptor.save_transcript_to_file(transcript_data, args.output)
            print(f"字幕をファイル '{args.output}' に保存しました")
            
            # テキスト形式でも保存
            text_output = args.output.rsplit('.', 1)[0] + '.txt'
            with open(text_output, 'w', encoding='utf-8') as f:
                f.write(YouTubeTranscriptor.get_transcript_text(
                    transcript_data, args.timestamps
                ))
            print(f"テキスト形式を '{text_output}' に保存しました")
        else:
            # 標準出力に表示
            text = YouTubeTranscriptor.get_transcript_text(transcript_data, args.timestamps)
            print("\n========== 字幕内容 ==========\n")
            print(text)
            print("\n==============================\n")

    except ValueError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    except TranscriptsDisabled:
        print(f"エラー: このビデオには字幕が無効になっています", file=sys.stderr)
        return 1
    except NoTranscriptFound as e:
        if args.translate:
            print(f"エラー: 言語 '{args.language}' の字幕が見つからず、他の言語からの翻訳も失敗しました", file=sys.stderr)
        else:
            print(f"エラー: 言語 '{args.language}' の字幕が見つかりません", file=sys.stderr)
            print("ヒント: -t または --translate オプションを使用すると、自動翻訳を試みます", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"予期せぬエラー: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
