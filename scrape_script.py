import pandas as pd
import time
import os

# 1. 名簿(target_list.txt)を読み込む
if not os.path.exists("target_list.txt"):
    print("エラー: target_list.txt が見つかりません。")
    exit()

with open("target_list.txt", "r", encoding="utf-8") as f:
    jockeys = [line.strip() for line in f if line.strip()]

# 2. ジョッキーごとにループ（同時並行的に処理）
for target_name in jockeys:
    print(f"--- {target_name} のデータを収集中... ---")
    all_data = []
    
    # 2021年の第1レースから2000レース分を調査（時間がかかります）
    for i in range(202101010101, 202101010101 + 2000):
        url = f"https://db.netkeiba.com/race/{i}/"
        try:
            dfs = pd.read_html(url)
            df = dfs[0]
            
            # そのレースに指定のジョッキーがいたら抜き出す
            found = df[df['騎手'].str.contains(target_name, na=False)].copy()
            
            if not found.empty:
                all_data.append(found)
                print(f"【発見】{target_name}: レースID {i}")
            
            time.sleep(1) # サーバーへのマナー
        except Exception:
            continue

    # 3. ジョッキーごとのファイル名（例：川田将雅_data.csv）で保存
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        filename = f"{target_name}_data.csv"
        final_df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"【完了】{filename} を作成しました。")

print("すべてのジョッキーの処理が終了しました。")
