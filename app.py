import streamlit as st
import sqlite3
import random

# --- КОНФИГУРАЦИЯ СТРАНИЦЫ ---
st.set_page_config(page_title="Magic English", page_icon="✨", layout="centered")

# --- СТИЛИЗАЦИЯ (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Montserrat', sans-serif;
        color: white;
    }
    
    .stButton>button {
        border-radius: 20px;
        border: none;
        background-color: #ff4b2b;
        color: white;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #ff416c;
        transform: scale(1.05);
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .word-card {
        background: rgba(255, 255, 255, 0.1);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- РАБОТА С БАЗОЙ ДАННЫХ ---
conn = sqlite3.connect('words_db.sqlite', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS dict (word TEXT, trans TEXT, cat TEXT)')
conn.commit()

# --- САЙДБАР (МЕНЮ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3898/3898082.png", width=100)
    st.title("Меню")
    choice = st.radio("Куда отправимся?", ["🏠 Главная", "➕ Добавить слова", "🧠 Тренировка", "📚 Весь словарь"])

# --- ЛОГИКА ПРИЛОЖЕНИЯ ---

if choice == "🏠 Главная":
    st.markdown("<h1 style='text-align: center;'>✨ Magic English ✨</h1>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/free-vector/learning-concept-illustration_114360-1107.jpg", use_container_width=True)
    st.write("### Добро пожаловать! Это приложение поможет тебе выучить английский играючи. Загляни в меню слева, чтобы начать!")

elif choice == "➕ Добавить слова":
    st.markdown("## ✏️ Новое знание")
    with st.container():
        word = st.text_input("Слово на английском")
        trans = st.text_input("Перевод на русском")
        cat = st.selectbox("Категория", ["Общее", "Глаголы", "Еда", "Путешествия"])
        submit = st.button("Сохранить в базу 💾")
        
        if submit:
            if word and trans:
                c.execute('INSERT INTO dict VALUES (?,?,?)', (word, trans, cat))
                conn.commit()
                st.balloons()
                st.success(f"Готово! '{word}' теперь в твоем списке!")
            else:
                st.error("Заполни оба поля!")

elif choice == "🧠 Тренировка":
    st.markdown("## 🧠 Проверка знаний")
    c.execute('SELECT * FROM dict')
    data = c.fetchall()

    if data:
        if 'card_idx' not in st.session_state:
            st.session_state.card_idx = random.randint(0, len(data) - 1)

        current_word = data[st.session_state.card_idx]

        st.markdown(f"""
            <div class="word-card">
                <h1 style='color: #FFD700;'>{current_word[0]}</h1>
                <p>Категория: {current_word[2]}</p>
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("👁️ Показать перевод"):
                st.markdown(f"<h3 style='text-align: center; color: #00FF7F;'>{current_word[1]}</h3>", unsafe_allow_html=True)
        
        with col2:
            if st.button("➡️ Следующее слово"):
                st.session_state.card_idx = random.randint(0, len(data) - 1)
                st.rerun()
    else:
        st.warning("⚠️ Твой словарь пока пуст. Добавь слов в меню!")

elif choice == "📚 Весь словарь":
    st.markdown("## 🗂️ Твоя коллекция")
    c.execute('SELECT * FROM dict')
    data = c.fetchall()
    if data:
        import pandas as pd
        df = pd.DataFrame(data, columns=['Слово', 'Перевод', 'Категория'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Тут пока ничего нет...")
