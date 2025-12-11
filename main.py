import requests
import time
import json
import os


def fetch_and_save_bangumi_data(username):
    url = f"https://api.bgm.tv/v0/users/{username}/collections"

    headers = {
        'User-Agent': 'hacci/anime-fetcher/1.1 (gemini-json-export)',
        'Accept': 'application/json'
    }

    params = {
        'subject_type': 2,  # 动画
        'type': 2,  # 看过
        'limit': 30,
        'offset': 0
    }

    # 保持之前的直连设置
    session = requests.Session()
    session.trust_env = False

    all_data = []  # 用于存储完整的字典数据
    print(f"正在抓取用户 {username} 的数据并准备保存...")

    while True:
        try:
            response = session.get(url, headers=headers, params=params, proxies={"http": None, "https": None})

            if response.status_code != 200:
                print(f"API 请求失败: {response.status_code}")
                break

            data = response.json()
            items = data.get('data', [])

            if not items:
                break

            for item in items:
                subject = item.get('subject', {})
                name = subject.get('name_cn') or subject.get('name')
                score = item.get('rate')

                # 构建结构化数据对象
                entry = {
                    "title": name,
                    "score": score if (score and score > 0) else None,  # 未评分存为 None
                    "tags": item.get('tags', [])  # 顺便把标签也抓下来，有助于推荐分析
                }
                all_data.append(entry)

            print(f"已收集 {len(all_data)} 条记录...")

            params['offset'] += params['limit']
            if len(items) < params['limit']:
                break

            time.sleep(0.3)

        except Exception as e:
            print(f"发生错误: {e}")
            break

    # --- 保存为 JSON 文件 (推荐给 Gem 使用) ---
    json_filename = 'bangumi_records.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        # ensure_ascii=False 保证中文正常显示，indent=4 保证格式美观
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    # --- 保存为 TXT 文件 (备用) ---
    txt_filename = 'bangumi_readable.txt'
    with open(txt_filename, 'w', encoding='utf-8') as f:
        for item in all_data:
            score_str = f"{item['score']}分" if item['score'] else "无评分"
            f.write(f"《{item['title']}》 - {score_str}\n")

    print(f"\n成功！文件已保存在当前目录下：")
    print(f"1. {os.path.abspath(json_filename)} (请上传这个给 Gem)")
    print(f"2. {os.path.abspath(txt_filename)}")


# 执行
fetch_and_save_bangumi_data('hacci')