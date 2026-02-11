import requests
from dateutil import parser
import json
import time
import os
import streamlit as st

WAIT_TIME = 20  # Tempo de espera em segundos

def get_comments_file_path():
    """Retorna o caminho do arquivo de comentários específico para o vídeo atual.
    Usa `comments_<VIDEO_ID>.json` quando houver `VIDEO_ID` na sessão;
    caso contrário, utiliza `comments.json` como padrão.
    """
    video_id = st.session_state.get('VIDEO_ID')
    if video_id:
        return f"comments_{video_id}.json"
    return "comments.json"

def comments_collect_visualization():
    st.title('Comments Collection')
    st.text(" If you already have a JSON file with comments, go to page 'Upload JSON' to upload it and skip this step.")
    st.text(" Tutorial video to register and save the GOOGLE_API_KEY: https://youtu.be/d4gPrwpzTkc ")
    
    if 'is_collecting' not in st.session_state:
        st.session_state['is_collecting'] = False
    if 'collection_count' not in st.session_state:
        st.session_state['collection_count'] = 0
    
    api_key = st.text_input("API Key (Google)", type= "password", key= "google_api_key")
    if api_key:
        st.session_state['GOOGLE_API_KEY'] = api_key
        
    video_input = st.text_input("Youtube Video URL or ID", placeholder="https://youtube.com/watch?v=...")
    
    if "youtube.com" in video_input or "youtu.be" in video_input:
        if "watch?v=" in video_input:
            video_id = video_input.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in video_input:
            video_id = video_input.split("youtu.be/")[1].split("?")[0]
    else:
        video_id = video_input
    
    if video_id:
        st.session_state['VIDEO_ID'] = video_id

    start_fresh = True

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Start Collection", type="secondary", disabled=st.session_state['is_collecting']):
            if not api_key or not video_id:
                st.error("Please provide both API Key and Video ID")
            else:
                st.session_state['GOOGLE_API_KEY'] = api_key
                st.session_state['VIDEO_ID'] = video_id
                if start_fresh:
                    save_comments([])
                    st.session_state['collection_count'] = 0
                
                live_chat_id, live_start_time_utc = get_live_details()
                
                if live_chat_id and live_start_time_utc:
                    st.session_state['is_collecting'] = True
                    st.session_state['live_chat_id'] = live_chat_id
                    st.session_state['live_start_time_utc'] = live_start_time_utc
                    st.success("Collection started! Click 'Stop Collection' to stop.")
                    st.rerun()
                else:
                    st.error(" This is not an active live stream. Only live streams are supported for comment collection.")
                    st.info(" Please provide a Video ID from an active YouTube live stream.")
    
    with col2:
        if st.button("Stop Collection", type="primary", disabled=not st.session_state['is_collecting']):
            st.session_state['is_collecting'] = False
            st.success(f"Collection stopped! Total comments collected: {st.session_state['collection_count']}")
            st.rerun()
    
    if st.session_state['is_collecting']:
        st.info(f"Collecting... Total comments so far: {st.session_state['collection_count']}")
        
        live_chat_id = st.session_state.get('live_chat_id')
        live_start_time_utc = st.session_state.get('live_start_time_utc')
        
        if live_chat_id and live_start_time_utc:
            new_comments = get_chat_messages(live_chat_id, live_start_time_utc)
            new_count = append_new_comments(new_comments)
            st.session_state['collection_count'] += new_count
            
            if new_count > 0:
                st.success(f"Added {new_count} new comments")
            
            time.sleep(WAIT_TIME)
            st.rerun()
    
    
    st.divider()
    comments = load_existing_comments()
    if comments:
        json_string = json.dumps(comments, indent=2, ensure_ascii=False)
        
        download_name = f"comments_{st.session_state.get('VIDEO_ID','')}.json" if st.session_state.get('VIDEO_ID') else "comments.json"
        st.download_button(
            label="Download Collected Comments",
            data=json_string,
            file_name=download_name,
            mime="application/json"
        )
            

def get_live_details():
    api_key = st.session_state.get('GOOGLE_API_KEY')
    video_id = st.session_state.get('VIDEO_ID')
    
    url = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={video_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    
    if "items" in data and len(data["items"]) > 0:
        if "liveStreamingDetails" in data["items"][0]:
            live_details = data["items"][0]["liveStreamingDetails"]
            if "actualStartTime" in live_details:
                live_start_time = live_details["actualStartTime"]
                return live_details.get("activeLiveChatId"), parser.isoparse(live_start_time)
    return None, None

def get_chat_messages(live_chat_id, live_start_time_utc):
    """Coleta mensagens de chat ao vivo do YouTube"""
    comments_list = []
    api_key = st.session_state.get('GOOGLE_API_KEY')
    chat_url = f"https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={live_chat_id}&part=snippet,authorDetails&maxResults=200&key={api_key}"
    chat_response = requests.get(chat_url)
    chat_data = chat_response.json()

    if "items" in chat_data:
        for item in chat_data["items"]:
            comment_id = item.get("id")
            author = item["authorDetails"]["displayName"]
            try:
                message = item["snippet"]["displayMessage"]
            except:
                message = ""
            timestamp = item["snippet"].get("publishedAt")
            
            if not timestamp or not comment_id:
                
                continue 

            message_time_utc = parser.isoparse(timestamp)
            
            time_elapsed = message_time_utc - live_start_time_utc
            
            time_elapsed_str = str(time_elapsed).split('.')[0]
            
            comment_entry = {
                "id": comment_id,
                "time_elapsed": time_elapsed_str,
                "author": author,
                "message": message
            }
            comments_list.append(comment_entry)
    return comments_list

def load_existing_comments():
    try:
        file_path = get_comments_file_path()
        with open(file_path, 'r', encoding='utf-8') as f:
            if f.read(1):
                f.seek(0)  # Volta para o início do arquivo
                return json.load(f)
            else:
                return []  # Arquivo vazio
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Arquivo não encontrado ou corrompido

def save_comments(comments_list):
    file_path = get_comments_file_path()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(comments_list, f, ensure_ascii=False, indent=4)

def append_new_comments(new_comments):
    existing_comments = load_existing_comments()
    existing_ids = {comment.get('id') for comment in existing_comments if 'id' in comment}
    
    new_comments_filtered = [comment for comment in new_comments if comment['id'] not in existing_ids]
    
    existing_comments.extend(new_comments_filtered)
    save_comments(existing_comments)
    
    return len(new_comments_filtered)  # Retorna a quantidade de novos comentários

# Loop para coletar e salvar comentários
#if __name__ == "__main__":
#    try:
#        while True:
#            live_chat_id, live_start_time_utc = get_live_details()
#            if live_chat_id and live_start_time_utc:
#                new_comments = get_chat_messages(live_chat_id, live_start_time_utc)
#                new_count = append_new_comments(new_comments)
#                print(f"Coletado e adicionado {new_count} novos comentários.")
#            else:
#                print("Não foi possível obter os detalhes da live ou o chat ao vivo. Verifique se o vídeo está ao vivo e se os detalhes estão disponíveis.")
            
#            time.sleep(WAIT_TIME)
#    except KeyboardInterrupt:
#        print("\n Collection stopped by user")