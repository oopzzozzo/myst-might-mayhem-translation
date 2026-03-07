# Translation History: Myst, Might, Mayhem (怪力亂神)

This document records the translation process of the web novel "Myst, Might, Mayhem" from English to Traditional Chinese.

## Project Overview
- **Total Chapters:** 311 (Prologue to Chapter 310)
- **Target Language:** Traditional Chinese (正體中文)
- **Style:** Dramatic, concise martial arts novel style (Wuxia/Xianxia)
- **GitHub Repository:** [oopzzozzo/myst-might-mayhem-translation](https://github.com/oopzzozzo/myst-might-mayhem-translation)

## Translation Methodology

### 1. Manual Chat Translation (Initial Batch)
- **Chapters:** 0 – 110
- **Model:** Gemini 2.0 Flash
- **Method:** Translated in manual batches within the chat environment to establish terminology and tone.

### 2. Automated Script v1
- **Chapters:** 111 – 131
- **Model:** Gemini 2.5 Flash (Internal Experimental)
- **Method:** Python script `watch_and_translate.py` using the Gemini API.

### 3. Automated Script v2 (Claude Code)
- **Chapters:** 132 – 244
- **Model:** Claude Sonnet 3.5
- **Method:** Transitioned to using `claude -p` for higher reliability and bypassing Gemini API rate limits. Automatically committed and pushed to GitHub.

### 4. Manual Chat Translation (Final Batch)
- **Chapters:** 245 – 310 (The End)
- **Model:** Gemini 2.0 Flash
- **Method:** Final manual batch translation to conclude the series and ensure high-quality finishing.

## Terminology Reference
Consistent terminology was maintained throughout the project using official names from Webtoon where possible:
- **木景雲** (Mok Gyeong-un)
- **大然木劍庄** (Yeon Mok Sword Manor)
- **虛空** (Void)
- **天地會** (Heaven & Earth Society)
- **屍血谷** (Corpse Blood Valley)
- **太殺閣** (Primal Killing Pavilion)
- **慶進大君** (Prince Gyeongjin)
- **虛空之陽** (Void Sun)
