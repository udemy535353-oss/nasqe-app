import os
import tkinter as tk
from tkinter import filedialog, Listbox
from tkinter import ttk
import pygame
import pandas as pd
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("ML Destekli Müzik Çalar")
        self.root.geometry("900x600")

        pygame.init()
        pygame.mixer.init()

        self.music_library_path = ""
        self.music_files = []
        self.music_data = pd.DataFrame()
        self.similarity_matrix = None
        self.current_song_index = -1
        self.paused = False
        # Öneri listesindeki şarkıların orjinal index'lerini saklamak için
        self.recommendation_indices = []

        # --- Arayüz Elementleri ---
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, padx=10, fill=tk.X)

        self.library_label = tk.Label(top_frame, text="Müzik Kütüphanesi Yüklenmedi", font=("Helvetica", 10))
        self.library_label.pack(side=tk.LEFT, padx=5)
        
        library_button = tk.Button(top_frame, text="Kütüphane Seç", command=self.load_music_library)
        library_button.pack(side=tk.RIGHT)

        center_frame = tk.Frame(self.root)
        center_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        library_list_frame = tk.Frame(center_frame)
        library_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(library_list_frame, text="Tüm Şarkılar", font=("Helvetica", 12, "bold")).pack()
        self.library_listbox = Listbox(library_list_frame, selectbackground="#3498db", selectforeground="white", font=("Helvetica", 10))
        self.library_listbox.pack(fill=tk.BOTH, expand=True)
        self.library_listbox.bind('<Double-1>', self.play_selected_song)

        recommender_list_frame = tk.Frame(center_frame)
        recommender_list_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(recommender_list_frame, text="🎵 Önerilenler", font=("Helvetica", 12, "bold")).pack()
        self.recommend_listbox = Listbox(recommender_list_frame, selectbackground="#2ecc71", selectforeground="white", font=("Helvetica", 10))
        self.recommend_listbox.pack(fill=tk.BOTH, expand=True)
        self.recommend_listbox.bind('<Double-1>', self.play_selected_recommendation)

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(pady=20)

        self.current_song_label = tk.Label(bottom_frame, text="Şu An Çalan: -", font=("Helvetica", 11, "italic"), wraplength=400)
        self.current_song_label.pack(pady=10)

        control_frame = tk.Frame(bottom_frame)
        control_frame.pack()

        self.prev_button = tk.Button(control_frame, text="⏮️", command=self.prev_song)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.play_button = tk.Button(control_frame, text="▶️", command=self.toggle_play_pause)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(control_frame, text="⏹️", command=self.stop_music)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(control_frame, text="⏭️", command=self.next_song)
        self.next_button.pack(side=tk.LEFT, padx=5)

    def load_music_library(self):
        self.music_library_path = filedialog.askdirectory()
        if not self.music_library_path:
            return

        self.library_label.config(text=f"Yüklendi: {os.path.basename(self.music_library_path)}")
        self.library_listbox.delete(0, tk.END)
        self.music_files.clear()
        all_metadata = []

        for root_dir, _, files in os.walk(self.music_library_path):
            for file in files:
                if file.endswith(".mp3"):
                    file_path = os.path.join(root_dir, file)
                    self.music_files.append(file_path)
                    try:
                        audio = MP3(file_path, ID3=ID3)
                        genre_tag = audio.get('TCON')
                        genre = genre_tag.text[0] if genre_tag and genre_tag.text else "Unknown"
                        artist_tag = audio.get('TPE1')
                        artist = artist_tag.text[0] if artist_tag and artist_tag.text else "Unknown"
                        title_tag = audio.get('TIT2')
                        title = title_tag.text[0] if title_tag and title_tag.text else os.path.basename(file)
                    except ID3NoHeaderError:
                        genre, artist, title = "Unknown", "Unknown", os.path.basename(file)
                    
                    all_metadata.append({'path': file_path, 'title': title, 'artist': artist, 'genre': genre})
                    self.library_listbox.insert(tk.END, f"{artist} - {title}")
        
        if not all_metadata:
            print("HATA: Seçilen klasörde hiç .mp3 dosyası bulunamadı.")
            return

        self.music_data = pd.DataFrame(all_metadata)
        self.build_recommender_model()
        print("Müzik kütüphanesi yüklendi ve öneri modeli oluşturuldu.")

    def build_recommender_model(self):
        self.music_data['genre'] = self.music_data['genre'].fillna('Unknown')
        self.music_data['artist'] = self.music_data['artist'].fillna('Unknown')

        self.music_data['clean_artist'] = self.music_data['artist'].apply(lambda x: str(x).replace(' ', '').lower())
        self.music_data['clean_genre'] = self.music_data['genre'].apply(lambda x: str(x).replace(' ', '').lower())
        
        self.music_data['features'] = self.music_data['clean_artist'] + ' ' + self.music_data['clean_artist'] + ' ' + self.music_data['clean_genre']
        
        tfidf = TfidfVectorizer(stop_words='english')
        feature_matrix = tfidf.fit_transform(self.music_data['features'])
        
        self.similarity_matrix = cosine_similarity(feature_matrix, feature_matrix)
        print("Öneri modeli hem sanatçı hem de türe göre başarıyla oluşturuldu.")

    def get_recommendations(self, song_index, num_recommendations=5):
        if self.similarity_matrix is None or song_index >= len(self.similarity_matrix):
            return []
            
        similarity_scores = list(enumerate(self.similarity_matrix[song_index]))
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        recommended_indices = [i[0] for i in sorted_scores[1:num_recommendations+1]]
        return recommended_indices

    def play_music(self, song_index):
        if not (0 <= song_index < len(self.music_files)):
            return
            
        self.current_song_index = song_index
        song_path = self.music_files[self.current_song_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        
        song_info = self.music_data.iloc[self.current_song_index]
        self.current_song_label.config(text=f"Şu An Çalan: {song_info['artist']} - {song_info['title']}")
        self.play_button.config(text="⏸️")
        self.paused = False
        self.library_listbox.selection_clear(0, tk.END)
        self.library_listbox.selection_set(self.current_song_index)

        self.recommend_listbox.delete(0, tk.END)
        self.recommendation_indices = self.get_recommendations(self.current_song_index)
        for idx in self.recommendation_indices:
            rec_info = self.music_data.iloc[idx]
            self.recommend_listbox.insert(tk.END, f"{rec_info['artist']} - {rec_info['title']}")

    def toggle_play_pause(self):
        if self.current_song_index == -1: return
        if self.paused:
            pygame.mixer.music.unpause()
            self.play_button.config(text="⏸️")
            self.paused = False
        else:
            pygame.mixer.music.pause()
            self.play_button.config(text="▶️")
            self.paused = True
    
    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_song_label.config(text="Şu An Çalan: -")
        self.current_song_index = -1
        self.play_button.config(text="▶️")

    def next_song(self):
        if self.current_song_index != -1 and self.music_files:
            next_index = (self.current_song_index + 1) % len(self.music_files)
            self.play_music(next_index)

    def prev_song(self):
        if self.current_song_index != -1 and self.music_files:
            prev_index = (self.current_song_index - 1) % len(self.music_files)
            self.play_music(prev_index)

    def play_selected_song(self, event):
        selected_indices = self.library_listbox.curselection()
        if selected_indices:
            self.play_music(selected_indices[0])

    def play_selected_recommendation(self, event):
        selected_indices = self.recommend_listbox.curselection()
        if selected_indices and self.recommendation_indices:
            original_index_to_play = self.recommendation_indices[selected_indices[0]]
            self.play_music(original_index_to_play)

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()