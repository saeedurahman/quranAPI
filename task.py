from fastapi import FastAPI
import pandas as pd
import re
import unicodedata

app = FastAPI()

# عربی اعراب (زبر، زیر، پیش) ہٹانے کا فنکشن
# def remove_tashkeel(text: str) -> str:
#     # اعراب کو ہٹانے کے لئے ایک ریگولر ایکسپریشن
#     return re.sub(r'[\u064B-\u0652\u0670\u06D6\u06D7\u06D8\u06D9\u06DA\u06DB\u06DC\u06DD\u06DE\u06DF\u06E0\u06E1\u06E2\u06E3\u06E4\u06E5\u06E6\u06E7\u06E8\u06E9\u06EA\u06EB\u06EC\u06ED\u06EE\u06EF\u06F0\u06F1\u06F2\u06F3\u06F4\u06F5\u06F6\u06F7\u06F8\u06F9\u06FA\u06FB\u06FC\u06FD\u06FE\u06FF]', '', text)

# # عربی حروف کو نارملائز کرنے کا فنکشن (مختلف حالتوں کو ایک ہی شکل میں تبدیل کرنا)
# def normalize_arabic(text: str) -> str:
#     # عربی حروف کو یونیکوڈ نارملائز کریں
#     normalized_text = unicodedata.normalize('NFKC', text)
#     # بعض اوقات الفاظ میں مختلف اسپیس کی علامات ہو سکتی ہیں، انہیں بھی صاف کریں
#     normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()
#     return normalized_text

def load_surahs():
    file_path = "QuranDaTa.xlsx"
    df = pd.read_excel(file_path, dtype=str)
    return df

quran_data = load_surahs()

@app.get("/")
async def root():
    return {"message": "Welcome to the Quran Surah API"}

# سورت کا نام فراہم کریں
@app.get("/surah/{sura_id}")
async def get_surah_name(sura_id: str):  
    surah = quran_data[quran_data["SuraID"] == sura_id]
    if surah.empty:
        return {"error": f"Surah with ID {sura_id} not found"}

    return {
        "Surah Name (Urdu)": surah.iloc[0]["SurahNameU"],
        "Surah Name (English)": surah.iloc[0]["SurahNameE"]
    }

# مخصوص آیت فراہم کریں
# صرف عربی آیات فراہم کریں
@app.get("/surah/{sura_id}/get_arabic_Ayah")
async def get_surah_arabic(sura_id: str):
    surah = quran_data[quran_data["SuraID"] == sura_id]
    if surah.empty:
        return {"error": f"Surah with ID {sura_id} not found"}

    result = []
    for _, row in surah.iterrows():
        result.append({
            "AyaNo": row["AyaNo"],
            "ArabicText": row["ArabicText"]
        })

    return {
        "Surah Name (Urdu)": surah.iloc[0]["SurahNameU"],
        "Surah Name (English)": surah.iloc[0]["SurahNameE"],
        "Ayahs": result
    }

# آیات اور ترجمے فراہم کریں
@app.get("/surah/{sura_id}/get_Ayah_with_translations")
async def get_surah_with_translations(sura_id: str):
    surah = quran_data[quran_data["SuraID"] == sura_id]
    if surah.empty:
        return {"error": f"Surah with ID {sura_id} not found"}

    result = []
    for _, row in surah.iterrows():
        result.append({
            "AyaNo": row["AyaNo"],
            "ArabicText": row["ArabicText"],
            "Translation (Fateh Muhammad Jalandhri)": row["Fateh Muhammad Jalandhri"],
            "Translation (Mehmood ul Hassan)": row["Mehmood ul Hassan"]
        })

    return {
        "Surah Name (Urdu)": surah.iloc[0]["SurahNameU"],
        "Surah Name (English)": surah.iloc[0]["SurahNameE"],
        "Ayahs": result
    }


# مکمل سورت کا ڈیٹا فراہم کریں
@app.get("/surah/{sura_id}/all")
async def get_surah_all(sura_id: str):
    surah = quran_data[quran_data["SuraID"] == sura_id]
    if surah.empty:
        return {"error": f"Surah with ID {sura_id} not found"}

    result = []
    for _, row in surah.iterrows():
        result.append({
            "AyaNo": row["AyaNo"],
            "ArabicText": row["ArabicText"],
            "Translation (Fateh Muhammad Jalandhri)": row["Fateh Muhammad Jalandhri"],
            "Translation (Mehmood ul Hassan)": row["Mehmood ul Hassan"]
        })

    return {
        "Surah Name (Urdu)": surah.iloc[0]["SurahNameU"],
        "Surah Name (English)": surah.iloc[0]["SurahNameE"],
        "Ayahs": result
    }

# @app.get("/search/arabic/")
# async def search_arabic(keyword: str):
#     # مطلوبہ لفظ کو نارملائز اور حرکات ہٹا کر صاف کریں
#     keyword = normalize_arabic(keyword.strip())
#     keyword = remove_tashkeel(keyword)

#     # عربی متن میں سرچ کریں
#     search_results = quran_data[quran_data["ArabicText"].str.contains(keyword, na=False, regex=True)]

#     if search_results.empty:
#         return {"error": f"No results found for '{keyword}' in Arabic text"}

#     result = []
#     for _, row in search_results.iterrows():
#         result.append({
#             "SuraID": row["SuraID"],
#             "AyaNo": row["AyaNo"],
#             "ArabicText": row["ArabicText"]
#         })
    
#     return {"Results": result}


# اردو ترجمہ میں تلاش کریں
@app.get("/search/urdu/")
async def search_urdu(keyword: str):
    keyword = keyword.strip()

    search_results = quran_data[
        (quran_data["Fateh Muhammad Jalandhri"].str.contains(keyword, na=False, regex=True)) |
        (quran_data["Mehmood ul Hassan"].str.contains(keyword, na=False, regex=True))
    ]

    if search_results.empty:
        return {"error": f"No results found for '{keyword}' in Urdu translation"}

    result = []
    for _, row in search_results.iterrows():
        result.append({
            "SuraID": row["SuraID"],
            "AyaNo": row["AyaNo"],
            "ArabicText": row["ArabicText"],
            "Translation (Fateh Muhammad Jalandhri)": row["Fateh Muhammad Jalandhri"],
            "Translation (Mehmood ul Hassan)": row["Mehmood ul Hassan"]
        })
    
    return {"Results": result}