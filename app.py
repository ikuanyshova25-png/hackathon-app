    if data:
        if 'card_idx' not in st.session_state:
            st.session_state.card_idx = random.randint(0, len(data)-1)
        
        current_word = data[st.session_state.card_idx]
        
        st.info(f"### Слово: {current_word[0]}")
        if st.button("Показать перевод"):
            st.success(f"Перевод: {current_word[1]}")
            st.caption(f"Категория: {current_word[2]}")
        
        if st.button("Следующее слово"):
            st.session_state.card_idx = random.randint(0, len(data)-1)
            st.rerun()
    else:
        st.warning("Словарь пуст. Добавьте слова в меню слева.")
