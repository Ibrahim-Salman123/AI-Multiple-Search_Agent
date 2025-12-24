
# from googlesearch import search
# for result in search("machine learning", num_results=3):
#     print(result)






import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.youtube.search import YouTubeSearchTool
import re
from deep_translator import GoogleTranslator
import tempfile
from gtts import gTTS
import os

# --- Custom CSS ---
st.markdown("""
<style>
.corner-image { position: fixed; top: 0; left: 0; z-index: 9999; width: 400px; height: 600px; }
.center-container { display: flex; justify-content: center; align-items: center; margin-top: 20px; }
div.stButton > button:first-child {
    background-color: blue !important;
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 0.6em 1.2em;
}
div.stButton > button:hover {
    background-color: green !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# --- Centered Title ---
st.markdown("""
<h1 style="font-size: 2.25rem; text-align: center;">AI Multiple Search Agent</h1>
<p style="font-size: 1.1rem; color: green; font-weight: bold; text-align: center;">Text, Videos, Voice & Translation</p>
""", unsafe_allow_html=True)

# --- Language Codes ---
lang_codes = {
    'English': 'en', 'Chinese': 'zh-CN', 'Hindi': 'hi', 'Spanish': 'es',
    'Russian': 'ru', 'Japanese': 'ja', 'Turkish': 'tr', 'Korean': 'ko',
    'German': 'de', 'Urdu': 'ur', 'Arabic': 'ar'
}

# --- Sidebar ---
with st.sidebar:
    st.title("Welcome")
    new_chat = st.button("+ New Chat")
    if new_chat:
        st.session_state.clear()
        st.rerun()

    language = st.selectbox('Choose Language:',
                            ['English', 'Chinese', 'Arabic', 'Hindi', 'Urdu', 'Russian',
                             'Turkish', 'Korean', 'German'])

    # --- Sidebar Image (Smaller Size) ---
    st.image("pic.png", width=180)

# --- Centered Input Section ---
st.markdown("<div class='center-container'>", unsafe_allow_html=True)
query = st.text_input('How may I assist you?', key="search_box")
st.markdown("</div>", unsafe_allow_html=True)

# --- Search Logic ---
if st.button('Search') and query:
    with st.spinner('Searching...'):
        try:
            translated_query = GoogleTranslator(source='auto', target=lang_codes[language]).translate(query)
        except:
            translated_query = query

        st.info(f"🔍 Searching for: '{query}' in {language}")

        # --- WEB SEARCH ---
        try:
            info = DuckDuckGoSearchRun().run(translated_query)
            try:
                translated_info = GoogleTranslator(source='auto', target=lang_codes[language]).translate(str(info))
            except:
                translated_info = info
            st.write(f"**📝 Text Results ({language}):**")
            st.write(translated_info)

            # --- Voice Output (AI Speaks) ---
            try:
                tts = gTTS(translated_info, lang=lang_codes[language])  # Complete text for voice
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    temp_path = fp.name
                    tts.save(temp_path)
                st.audio(temp_path, format="audio/mp3")
            except Exception as e:
                st.warning(f"Voice output unavailable: {e}")

        except Exception as e:
            st.error(f"Error in web search: {e}")

        # --- YOUTUBE SEARCH ---
        try:
            video_results = YouTubeSearchTool().run(translated_query)
            st.write(f"**🎥 Video Results ({language}):**")
            video_ids = re.findall(r'v=([a-zA-Z0-9_-]+)', video_results)
            if video_ids:
                for i, video_id in enumerate(video_ids[:3]):
                    st.video(f"https://youtube.com/watch?v={video_id}")
            else:
                st.warning("No videos found. Try another search term.")
        except Exception as e:
            st.error(f"Error in YouTube search: {e}")




























# from langchain_community.tools import Tool
# from langgraph.graph import StateGraph
# import requests
#
# weather = Tool("weather", lambda p: requests.get(f"https://wttr.in/{p}?format=3", timeout=10).text, "Real-time weather")
# graph = StateGraph(dict)
# graph.add_node("weather", lambda s: {"query": s["query"], "output": weather.run(s["query"])})
# graph.set_entry_point("weather")
# agent = graph.compile()
# print(agent.invoke({"query":"Pakistan-Lahore"})["output"])
# print(agent.invoke({"query":"USA-Chicago"})["output"])








#






