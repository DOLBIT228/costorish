import streamlit as st
import pandas as pd
import requests
from database import get_connection, init_db
from pdf_generator import generate_pdf

init_db()
conn = get_connection()
cur = conn.cursor()

st.set_page_config(layout="wide")
st.title("💍 CRM Кошторис Обручок")

tab1, tab2, tab3 = st.tabs(["Менеджер", "Адмінка", "Історія"])

# ================= NBU =================

def update_usd():
    try:
        r = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json", timeout=5)
        usd = next(x for x in r.json() if x["cc"] == "USD")["rate"]
        cur.execute("UPDATE settings SET usd_rate=? WHERE id=1", (usd,))
        conn.commit()
    except:
        pass

update_usd()

# ================= ADMIN =================

with tab2:
    st.header("Адмін панель")

    st.subheader("Додати метал")
    name = st.text_input("Назва металу")
    price = st.number_input("Ціна за грам (₴)", 0.0)

    if st.button("Додати метал"):
        cur.execute("INSERT INTO metals(name,price_per_gram) VALUES(?,?)", (name, price))
        conn.commit()
        st.success("Метал додано")

    st.subheader("Додати каміння")
    sname = st.text_input("Назва каміння")
    sprice = st.number_input("Ціна каміння (₴)", 0.0)

    if st.button("Додати каміння"):
        cur.execute("INSERT INTO stones(name,price) VALUES(?,?)", (sname, sprice))
        conn.commit()
        st.success("Каміння додано")

    st.subheader("Вартість роботи ювеліра")
    jeweler = st.number_input("₴ за грам", 0.0)

    if st.button("Оновити ціну роботи"):
        cur.execute("UPDATE settings SET jeweler_price_per_gram=? WHERE id=1", (jeweler,))
        conn.commit()
        st.success("Оновлено")

# ================= MANAGER =================

with tab1:
    st.header("Створити кошторис")

    metals = pd.read_sql("SELECT * FROM metals", conn)
    stones = pd.read_sql("SELECT * FROM stones", conn)
    settings = pd.read_sql("SELECT * FROM settings", conn)

    if metals.empty:
        st.warning("Додайте метали в адмінці")
    else:
        metal = st.selectbox("Метал", metals["name"])
        weight = st.number_input("Вага (г)", 0.0)

        stone = st.selectbox("Каміння", stones["name"]) if not stones.empty else None
        qty = st.number_input("Кількість камінців", 0)

        if st.button("Розрахувати"):
            metal_price = metals[metals["name"] == metal]["price_per_gram"].values[0]
            jeweler_price = settings["jeweler_price_per_gram"].values[0]

            metal_sum = weight * metal_price
            work_sum = weight * jeweler_price
            stone_sum = 0

            if stone:
                stone_price = stones[stones["name"] == stone]["price"].values[0]
                stone_sum = stone_price * qty

            total = metal_sum + work_sum + stone_sum

            st.success(f"Загальна сума: {total:.2f} ₴")

            cur.execute(
                "INSERT INTO estimates(metal,weight,stones,total) VALUES(?,?,?,?)",
                (metal, weight, stone, total)
            )
            conn.commit()

            pdf_data = {
                "Метал": metal,
                "Вага": f"{weight} г",
                "Метал вартість": f"{metal_sum:.2f}",
                "Робота": f"{work_sum:.2f}",
                "Каміння": f"{stone_sum:.2f}",
                "Разом": f"{total:.2f}"
            }

            pdf = generate_pdf(pdf_data)
            st.download_button("⬇️ Завантажити PDF", pdf, "koshtorys.pdf")

# ================= HISTORY =================

with tab3:
    st.header("Історія кошторисів")
    history = pd.read_sql("SELECT * FROM estimates ORDER BY id DESC", conn)
    st.dataframe(history)