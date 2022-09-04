from re import search
from youtubesearchpython import VideosSearch
from audioplayer import AudioPlayer
from tkinter import *
import youtube_dl
import os
from customtkinter import *
import time

set_appearance_mode("dark")  # Modes: system (default), light, dark
set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = CTk() 
root.title("TOM")
root.resizable(False, False)

def add_song():
    add_song_win = CTkToplevel(root)
    add_song_win.geometry("400x240")

    get_song = CTkLabel(master=add_song_win, text='\n\n 노래 제목 :')
    get_song.pack()

    get_song_entry = CTkEntry(master=add_song_win)
    get_song_entry.pack()

    def search_song():
        song_name = get_song_entry.get()
        get_song.configure(text='\n\n 다운로드 중 : ')
        vs = VideosSearch(f"{song_name}", limit=1)
        vs = vs.result()
        # 영상 목록 여러개 보여줘서 선택 후 다운받게 하는 기능 추후에 제작  
        url = vs["result"][0]["link"]
        name = vs["result"][0]["title"]

        ydl_opts = {
                        "outtmpl": f"music/{name}",
                        "postprocessors": [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "192",
                            }
                        ],
                    }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:  # 다운로드
            ydl.download([url])
        
        get_song.configure(text='\n\n다운로드 완료 :')
        add_song_win.destroy()

        # 플레이리스트 선택 창 만들고 진행 (다운로드 창은 삭제됨)

        choice_playlist = CTkToplevel(root)
        os_playlist = os.listdir("./playlist/")
        playlist_list = [] # 플레이리스트 이름만 있는 리스트  ex) ['playlist1', 'playlist2']
        
        for i in os_playlist:
            playlist_list.append(i.replace(".txt", ""))
        
        playlist = CTkComboBox(master=choice_playlist, values=playlist_list, command=None)
        playlist.pack()

        def save_it_playlist():
            save_to = playlist.get()
            print(save_to)
            print(os_playlist)
            with open(f'./playlist/{save_to}.txt', 'a', encoding='utf-8') as f:
                f.write(f"{name}\n")
            print('작성완료')

        select_playlist_btn = CTkButton(master=choice_playlist, text='선택', command=save_it_playlist)
        select_playlist_btn.pack()

    search_btn = CTkButton(master=add_song_win, text='검색', command=search_song)
    search_btn.pack()

add_song_btn = CTkButton(master=root, text='노래 추가', command=add_song)
add_song_btn.pack()

root.mainloop()
