import sys
import pandas as pd
import requests
from lxml import html
import time

# ★ここが重要：GitHub Actionsから「誰のデータを取るか」を受け取ります
if len(sys.argv) > 1:
    target_name = sys.argv[1]
else:
    target_name = "川田将雅"  # テスト用のデフォルト

print(f"=== {target_name} のデータ収集を開始します ===")

def scrape_jockey_data(name):
    # ここにマルさんが今まで使っていた「スクレイピングのメイン処理」を入れます
    # 2000レース回るループなど、今までのコードの中身をここに持ってきてください
    print(f"{name} のデータを取得中...")
    
    # 最後にCSVを保存する際の名前を固定します
    filename = f"{name}_data.csv"
    # df.to_csv(filename, index=False) 
    print(f"保存完了: {filename}")

# 実行
scrape_jockey_data(target_name)
