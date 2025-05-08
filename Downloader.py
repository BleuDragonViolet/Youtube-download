import os
import yt_dlp


def get_video_details(url):
    # Récupère les détails de la vidéo YouTube avec yt-dlp
    try:
        ydl_opts = {
            'quiet': True,
            'simulate': True,
            'extract_flat': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info
    except Exception as e:
        print("Une erreur s'est produite lors de la récupération des détails de la vidéo :", e)
        return None


def print_video_details(info):
    # Affiche les détails de la vidéo
    if info is not None:
        print("Titre :", info.get('title', 'Inconnu'))
        print("Nombre de vues :", info.get('view_count', 'Inconnu'))
        print("Durée :", info.get('duration', 'Inconnu'), "secondes")
        print("Note moyenne :", info.get('average_rating', 'Inconnu'))


def download_video(url, quality, only_audio):
    # Télécharge une vidéo YouTube
    output_path = os.path.join(os.path.dirname(__file__), 'data')  # Enregistre dans un sous-dossier "data" du script
    ydl_opts = {
        'format': 'bestaudio/best' if only_audio else ('best' if quality == 'high' else 'worst'),
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Téléchargement terminé !")
    except Exception as e:
        print("Une erreur s'est produite lors du téléchargement :", e)


def download_playlist(url, quality, only_audio):
    # Télécharge une playlist YouTube entière
    try:
        output_path = os.path.join(os.path.dirname(__file__), 'data')  # Enregistre dans un sous-dossier "data"
        ydl_opts = {
            'format': 'bestaudio/best' if only_audio else ('best' if quality == 'high' else 'worst'),
            'outtmpl': os.path.join(output_path, '%(playlist_title)s/%(title)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Téléchargement de la playlist terminé !")
    except Exception as e:
        print("Une erreur s'est produite lors du téléchargement de la playlist :", e)


def read_urls_from_file(filename):
    # Lit les URL de vidéos à partir d'un fichier .txt
    try:
        with open(filename, 'r') as file:
            urls = file.readlines()
        return urls
    except Exception as e:
        print("Une erreur s'est produite lors de la lecture du fichier :", e)
        return []


def help():
    # Affiche le menu d'aide
    print("Entrez '1' pour entrer une URL de vidéo YouTube.")
    print("Entrez '2' pour lire les URL de vidéos à partir d'un fichier .txt.")
    print("Entrez '3' pour entrer une URL de playlist YouTube.")


def main():
    # Point d'entrée principal du programme
    help()
    choice = input("Votre choix : ")
    quality = input("Choisissez la qualité de la vidéo (high/low) : ") == 'high'
    only_audio = input("Télécharger uniquement l'audio (yes/no) : ") == 'yes'

    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads', 'Youtube download', 'data')
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    if choice == '1':
        url = input("Entrez l'URL de la vidéo YouTube : ")
        info = get_video_details(url)
        print_video_details(info)
        download_video(url, quality, only_audio)
    elif choice == '2':
        filename = os.path.join(os.path.expanduser('~'), 'Downloads', 'Youtube download', 'url.txt')
        if os.path.exists(filename):
            urls = read_urls_from_file(filename)
            for url in urls:
                url = url.strip()
                info = get_video_details(url)
                print_video_details(info)
                download_video(url, quality, only_audio)
        else:
            print("Le fichier", filename, "n'existe pas.")
    elif choice == '3':
        url = input("Entrez l'URL de la playlist YouTube : ")
        download_playlist(url, quality, only_audio)


if __name__ == "__main__":
    main()
