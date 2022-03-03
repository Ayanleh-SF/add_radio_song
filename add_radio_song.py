"""
	Ajoute la musique jouée aléatoirement dans une playlist
	Entrée : Nom d'une playlist
	Sortie : None	
"""
import psutil
from pywinauto.application import Application
from time import sleep


def find_pid():
	for proc in psutil.process_iter():
		if proc.name() == "Spotify.exe":
			for k,v in proc.as_dict().items():
				if k == "cmdline" and v[0] == "Spotify.exe":
					spotify_pid = proc.as_dict()["pid"]

	return spotify_pid


def add_song(playlist_name):
	spotify_pid = find_pid()
	last_song = None

	app = Application(backend="uia").connect(process=spotify_pid)

	while True:
		sleep(60)
		song_name = app.windows()[0].window_text()
		
		if last_song != song_name or last_song == None:
			last_song = song_name

			app = Application(backend="uia").start("Spotify.exe")
			app = Application(backend="uia").connect(process=spotify_pid)

			if app.top_window().child_window(title="NE PAS AJOUTER", control_type="Button").exists():
				app.top_window().child_window(title="NE PAS AJOUTER", control_type="Button").click()


			app.top_window().child_window(best_match="Accueil").invoke()

			app.top_window().child_window(best_match="Rechercher").invoke()

			app.top_window().child_window(title="Artistes, titres ou podcasts", control_type="Edit").wait("enabled").set_text(text=song_name)
			
			app.top_window().child_window(title="Résultats de la recherche de titres", control_type="Table").child_window(best_match="Plus d'options pour", control_type="MenuItem").wait("enabled").invoke()
			
			app.top_window().child_window(title="Ajouter à la playlist", control_type="MenuItem").wait("enabled").invoke()

			if app.top_window().child_window(title=playlist_name, control_type="MenuItem").exists():
				app.top_window().child_window(title=playlist_name, control_type="MenuItem").invoke()


			app.top_window().minimize()


add_song("radio jpop") # En premier argument mettre le nom de la playlist (déjà créee au préalable)
