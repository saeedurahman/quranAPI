from fastapi import FastAPI
import pandas as pd
import re
import unicodedata

app = FastAPI()


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

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
