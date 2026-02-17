import streamlit as st
import pandas as pd
import json, requests
from database import conn, init
from pdf_generator import make_pdf

init()
c = conn()
cur = c.cursor()

st.set_page_config(layout="wide")
st.title("💍 Кошторис обручок")

manager, admin, history = st.tabs(["Менеджер","Адмінка","Історія"])

# -------- USD --------

def update_usd():
    try:
        r=requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json",timeout=5)
        rate=next(x for x in r.json() if x["cc"]=="USD")["rate"]
        cur.execute("UPDATE settings SET usd=? WHERE id=1",(rate,))
        c.commit()
    except:
        pass

update_usd()

# ================= ADMIN =================

with admin:
    st.header("Адмін")

    m=st.text_input("Метал")
    mp=st.number_input("₴/г",0.0)

    if st.button("Додати метал"):
        if m:
            cur.execute("INSERT INTO metals(name,price) VALUES(?,?)",(m,mp))
            c.commit()

    s=st.text_input("Каміння")
    sp=st.number_input("₴ каміння",0.0)

    if st.button("Додати каміння"):
        if s:
            cur.execute("INSERT INTO stones(name,price) VALUES(?,?)",(s,sp))
            c.commit()

    jw=st.number_input("Робота ювеліра ₴/г",0.0)

    if st.button("Зберегти роботу"):
        cur.execute("UPDATE settings SET jeweler=? WHERE id=1",(jw,))
        c.commit()

    st.dataframe(pd.read_sql("SELECT * FROM metals",c))
    st.dataframe(pd.read_sql("SELECT * FROM stones",c))

# ================= MANAGER =================

with manager:

    metals=pd.read_sql("SELECT * FROM metals",c)
    stones=pd.read_sql("SELECT * FROM stones",c)

    cur.execute("SELECT jeweler FROM settings WHERE id=1")
    jeweler=float(cur.fetchone()[0])

    if metals.empty or stones.empty:
        st.error("Додай метали та каміння в адмінці")
        st.stop()

    col1,col2=st.columns(2)

    with col1:
        size_w=st.text_input("Розмір жіночої")
        width_w=st.text_input("Ширина жіночої")
        thick_w=st.text_input("Товщина жіночої")
        weight_w=st.number_input("Вага жіночої",0.0)

    with col2:
        size_m=st.text_input("Розмір чоловічої")
        width_m=st.text_input("Ширина чоловічої")
        thick_m=st.text_input("Товщина чоловічої")
        weight_m=st.number_input("Вага чоловічої",0.0)

    metal=st.selectbox("Метал",metals["name"])
    stone=st.selectbox("Каміння",stones["name"])
    qty=st.number_input("Кількість камінців",0)

    if st.button("Згенерувати кошторис"):

        m=metals[metals["name"]==metal].iloc[0]
        s=stones[stones["name"]==stone].iloc[0]

        total_w=weight_w*m["price"]+weight_w*jeweler
        total_m=weight_m*m["price"]+weight_m*jeweler
        stone_sum=qty*s["price"]

        total=total_w+total_m+stone_sum

        rows=[
            {"type":"row","c1":"Розмір","c2":size_w,"c3":size_m},
            {"type":"row","c1":"Ширина","c2":width_w,"c3":width_m},
            {"type":"row","c1":"Товщина","c2":thick_w,"c3":thick_m},
            {"type":"section","title":"ЦІНОУТВОРЕННЯ"},
            {"type":"row","c1":"Метал","c2":metal,"c3":metal},
            {"type":"row","c1":"Вага","c2":weight_w,"c3":weight_m},
            {"type":"section","title":"КАМІНЦІ"},
            {"type":"row","c1":"Тип","c2":stone,"c3":stone},
            {"type":"row","c1":"Кількість","c2":qty,"c3":qty},
        ]

        pdf=make_pdf(rows,total)

        cur.execute("INSERT INTO estimates(data,total) VALUES(?,?)",(json.dumps(rows),total))
        c.commit()

        st.success(f"Разом: {total:.2f} ₴")
        st.download_button("⬇️ PDF",pdf,"koshtorys.pdf")

# ================= HISTORY =================

with history:
    st.dataframe(pd.read_sql("SELECT * FROM estimates ORDER BY id DESC",c))
