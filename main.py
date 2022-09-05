from re import search
from youtubesearchpython import VideosSearch
# from audioplayer import AudioPlayer
from playsound import playsound 
from tkinter import *
import youtube_dl
import os
from customtkinter import *

# 개인 설정 저장된걸로 불러오기 (setting/appearance_mode.txt, default_color_theme.txt)
# 홈 메뉴에서 설정 가능
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

def add_playlist():
    add_playlist_win = CTkToplevel(root)

    whatis_name = CTkLabel(master=add_playlist_win, text='재생목록의 이름을 작성해주세요.')
    whatis_name.pack()

    get_name = CTkEntry(master=add_playlist_win)
    get_name.pack()

    def make_playlist():
        playlist_name = get_name.get()
        open(f'./playlist/{playlist_name}.txt' , 'w').close()
        add_playlist_win.destory()
        
    make_btn = CTkButton(master=add_playlist_win, text='만들기', command=make_playlist)
    make_btn.pack()
    
def ready_delete_playlist():
    delete_pl_win = CTkToplevel(root)

    pl_label = CTkLabel(master=delete_pl_win, text='삭제할 재생목록을 선택해주세요.')
    pl_label.pack()

    os_playlist = os.listdir('./playlist/')
    playlist_list = [] # 플레이리스트 이름만 있는 리스트  ex) ['playlist1', 'playlist2']
        
    for i in os_playlist:
        playlist_list.append(i.replace(".txt", ""))

    playlist = CTkComboBox(master=delete_pl_win, values=playlist_list, command=None)
    playlist.pack()

    def delete_playlist():
        the_pl_name = playlist.get()
        os.remove(f'./playlist/{the_pl_name}.txt')
        delete_pl_win.destroy()

    accept_to_delete_btn = CTkButton(master=delete_pl_win, text='제거하기', command=delete_playlist)
    accept_to_delete_btn.pack()

def ready_play_song():
    play_song_win = CTkToplevel(root)

    pl_label = CTkLabel(master=play_song_win, text='재생할 재생목록을 선택해주세요.')
    pl_label.pack()

    os_playlist = os.listdir('./playlist/')
    playlist_list = [] # 플레이리스트 이름만 있는 리스트  ex) ['playlist1', 'playlist2']
        
    for i in os_playlist:
        playlist_list.append(i.replace(".txt", ""))

    playlist = CTkComboBox(master=play_song_win, values=playlist_list, command=None)
    playlist.pack()

    def play_song():
        the_playlist = playlist.get()
        with open(f'./playlist/{the_playlist}.txt', 'r', encoding='utf-8') as f:
            songs = f.readlines()
        
        play_song_win.destroy()
        song_setting = CTkToplevel(root)
        
        for i in songs:
            if "\n" in i:
                i = i.replace("\n", "")
            # AudioPlayer(f"./music/{i}.mp3").play(block=True) 
            playsound(f'./music/{i}.mp3') 

    play_btn = CTkButton(master=play_song_win, text='재생 시작', command=play_song)
    play_btn.pack()

add_song_btn = CTkButton(master=root, text='노래 추가', command=add_song)
add_song_btn.pack()

add_playlist_label = CTkLabel(master=root, text='\n')
add_playlist_label.pack()

add_playlist_btn = CTkButton(master=root, text='재생목록 추가', command=add_playlist)
add_playlist_btn.pack()

delete_playlist_btn = CTkButton(master=root, text='재생목록 삭제', command=ready_delete_playlist)
delete_playlist_btn.pack()

play_song_btn = CTkButton(master=root, text='노래 재생', command=ready_play_song)
play_song_btn.pack()

root.mainloop()
