import pandas as pd
import requests
import time
import io
import os

# --- 設定 ---
# target_list.txt (川田将雅) を読み込む
if os.path.exists('target_list.txt'):
    with open('target_list.txt', 'r', encoding='utf-8') as f:
        targets = [line.strip() for line in f if line.strip()]
else:
    targets = ["川田将雅"]

years = [2021, 2022, 2023, 2024, 2025, 2026]
places = [f"{i:02}" for i in range(1, 11)] # 全国10競馬場
output_file = "kawada_data.csv"
headers = {"User-Agent": "Mozilla/5.0"}

# 既存データの読み込み（続きからやるため）
if os.path.exists(output_file):
    final_df = pd.read_csv(output_file)
else:
    final_df = pd.DataFrame()

print(f"調査対象: {targets}")

count = 0
for year in years:
    for place in places:
        for kai in range(1, 7):
            for day in range(1, 13):
                for r in range(1, 13):
                    race_id = f"{year}{place}{kai:02}{day:02}{r:02}"
                    
                    # 取得済みならスキップ
                    if not final_df.empty and race_id in final_df['race_id'].astype(str).values:
                        continue

                    try:
                        url = f"https://db.netkeiba.com/race/{race_id}/"
                        res = requests.get(url, headers=headers, timeout=10)
                        res.encoding = res.apparent_encoding
                        
                        dfs = pd.read_html(io.StringIO(res.text))
                        if not dfs: continue
                        df = dfs[0]
                        
                        # 騎手の列に「川田将雅」がいるかチェック
                        pattern = '|'.join(targets)
                        if '騎手' in df.columns:
                            matched = df[df['騎手'].str.contains(pattern, na=False)]
                            
                            if not matched.empty:
                                matched = matched.copy()
                                matched['race_id'] = race_id
                                final_df = pd.concat([final_df, matched], ignore_index=True)
                                print(f"【発見】{race_id} のデータを保存しました")
                        
                        count += 1
                        time.sleep(1) # サーバーへのマナー
                        
                        # 1回の実行で100レース分チェックしたら終了（続きは明日）
                        if count >= 100:
                            final_df.to_csv(output_file, index=False, encoding="utf-8-sig")
                            print("本日の100件チェック完了。残りは明日自動で実行します。")
                            exit()
                            
                    except:
                        continue

# 全日程チェックが終わった場合
final_df.to_csv(output_file, index=False, encoding="utf-8-sig")
print("すべてのチェックが完了しました。")
