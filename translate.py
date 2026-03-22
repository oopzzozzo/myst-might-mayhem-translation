#!/usr/bin/env python3
"""
Translate Myst,Might,Mayhem English chapters → Traditional Chinese (怪力亂神)
Fluent Korean martial arts novel style, using established webtoon noun translations.
"""
import os
import sys
import time
import glob
import anthropic

import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("CLAUDE_CODE_OAUTH_TOKEN"))

GLOSSARY = """
## 專有名詞對照表（Proper Noun Glossary）

### 人物
- Mok Gyeong-un → 木景雲（主角）
- Cheong-ryeong → 青靈（寄宿於木景雲體內的靈體）
- Jang Neung-ak → 張能岳
- Wi So-yeon → 魏昭妍
- Xia Cailin → 夏彩琳
- Gao Zan → 高賛
- Shang Xiongbo → 尚雄博（外堂主）
- Cho Tae-cheong → 趙泰昌
- Dam Baek-ha → 譚白霞（第六血聖）
- Dam Ye-hwa → 譚藝花（前代第六血聖）
- Ma Ra-hyeon → 馬羅賢（混血千夫長）

### 稱號 / 綽號
- Sickle Demon → 鐮殺鬼
- Nine Blood Cult → 九血教
- Blood Saint（rank title within 九血教） → 血聖
- Northern Sect Blade King → 弒殺之王
- Three Eyes → 三眼
- Holy Fire Priestess / Saintess → 聖女（拜火教）
- Guyeo → 犰狳

### 門派 / 組織
- Mok Sword Manor → 然木劍庄
- Heaven & Earth Society → 天地會
- Corpse Blood Valley → 屍血谷
- Primal Killing Pavilion → 原殺閣
- Shadow Clan → 鬼影閣
- Embroidered Uniform Guard → 錦衣衛
- The Fourth Office（prison division of 錦衣衛） → 四所
- Six Offices Department → 六所部
- Shaolin Temple → 少林寺

### 地名 / 場所
- （no specific place name changes beyond the above）

### 武功 / 術法
- Gu Poison → 蠱毒
- Demon Sword → 惡則劍
- Blood Jade Hand → 血玉手
- Gal-jeo → 羯狙

### 物品 / 概念
- The Mark → 標記
- Diabolic Beast → 靈獸

### 皇室
- Prince Gyeongjin → 競進王
- Consort Ho → 胡貴人
- Lady Seo, the Imperial Noble Consort → 徐貴妃
"""

SYSTEM_PROMPT = f"""你是一位專業的武俠小說翻譯者，專門將韓國武俠小說翻譯成繁體中文。
你的翻譯風格應流暢自然，符合中文武俠小說的敘事節奏，避免逐字直譯的生硬感。

翻譯規則：
1. 使用繁體中文
2. 人名、地名、門派名稱必須嚴格按照下方對照表翻譯，不得自行創造
3. 對話使用「」，內心獨白使用『』，書信/系統文字使用【】
4. 武打動作、氣勢描寫要有韓式武俠的張力與節奏感
5. 刪除所有空白行，段落之間不留空行，保持緊湊的閱讀節奏
6. 只輸出翻譯結果，不要加任何說明或標注
7. 第一行為章節標題（繁中），之後直接接正文，中間不空行

{GLOSSARY}
"""

def get_output_filename(english_filename):
    """Map English filename (NNN_...) to existing Chinese filename."""
    basename = os.path.basename(english_filename)
    num = int(basename.split('_')[0])  # e.g. 001 → 1
    zh_num = num - 1  # Chinese is 0-indexed: 001→第000話
    zh_dir = '/home/pi/projects/novel/怪力亂神'
    pattern = os.path.join(zh_dir, f'第{zh_num:03d}話*.txt')
    matches = glob.glob(pattern)
    if matches:
        return matches[0]
    # fallback: construct filename
    return os.path.join(zh_dir, f'第{zh_num:03d}話.txt')

def translate_chapter(english_path):
    with open(english_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Remove excessive blank lines from source
    lines = [l for l in content.split('\n') if l.strip()]
    clean_content = '\n'.join(lines)

    msg = client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[{
            'role': 'user',
            'content': f'請翻譯以下章節：\n\n{clean_content}'
        }]
    )
    return msg.content[0].text.strip()

def main():
    en_dir = '/home/pi/projects/novel/Myst,Might,Mayhem'
    english_files = sorted(glob.glob(os.path.join(en_dir, '*.txt')))

    start_from = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    total = len(english_files)
    done = 0
    failed = []

    for en_file in english_files:
        num = int(os.path.basename(en_file).split('_')[0])
        if num < start_from:
            continue

        out_file = get_output_filename(en_file)
        chapter_name = os.path.basename(en_file)

        print(f'[{num:03d}/{total}] {chapter_name} → {os.path.basename(out_file)}', flush=True)

        try:
            translated = translate_chapter(en_file)
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(translated + '\n')
            done += 1
            print(f'  ✓ {len(translated)} chars', flush=True)
        except Exception as e:
            print(f'  ✗ ERROR: {e}', flush=True)
            failed.append((num, str(e)))
            time.sleep(5)

        time.sleep(0.5)  # small delay between API calls

    print(f'\nDone: {done}/{total} translated.')
    if failed:
        print(f'Failed: {failed}')

if __name__ == '__main__':
    main()
