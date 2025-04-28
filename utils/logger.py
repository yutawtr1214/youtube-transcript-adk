import logging
import os
from datetime import datetime

def setup_logger(name, log_dir='logs'):
    """
    ロガーの設定を行う関数
    
    Args:
        name: ロガーの名前
        log_dir: ログファイルを保存するディレクトリ
        
    Returns:
        設定済みのロガーインスタンス
    """
    # ログディレクトリが存在しない場合は作成
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 現在の日時を含むログファイル名を生成
    log_file = os.path.join(log_dir, f'{name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    
    # ロガーの設定
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # ファイルハンドラの設定
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # フォーマットの設定
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # ハンドラをロガーに追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
