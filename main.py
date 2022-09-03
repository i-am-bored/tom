from re import search
from youtubesearchpython import VideosSearch
from audioplayer import AudioPlayer
from tkinter import *
import youtube_dl
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk() 
root.title("TOM")
root.resizable(False, False)

def add_song():
    add_song_win = customtkinter.CTkToplevel(root)
    add_song_win.geometry("400x240")

    get_song = customtkinter.CTkLabel(master=add_song_win, text='\n\n 노래 제목 :')
    get_song.pack()

    get_song_entry = customtkinter.CTkEntry(master=add_song_win)
    get_song_entry.pack()

    def search_song():
        song_name = get_song_entry.get()
        vs = VideosSearch(f"{song_name}", limit=1)
        vs = vs.result()
        # 영상 목록 여러개 보여줘서 선택 후 다운받게 하는 기능 추후에 제작  
        url = vs["result"][0]["link"]
        get_song.config(text='다운로드 중 : ')

        ydl_opts = {
                        "outtmpl": f"music/{sn}",
                        "postprocessors": [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "192",
                            }
                        ],
                    }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    search_btn = customtkinter.CTkButton(master=add_song_win, text='검색', command=search_song)
    search_btn.pack()

add_song_btn = customtkinter.CTkButton(master=root, text='노래 추가', command=add_song)
add_song_btn.pack()

root.mainloop()
