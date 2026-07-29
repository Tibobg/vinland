import os
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import Picture
import base64

def extract_cover(file_path, output_dir):
    try:
        audio = OggVorbis(file_path)
        
        if 'metadata_block_picture' in audio.tags:
            # Décode la cover base64
            picture_data = audio.tags['metadata_block_picture'][0]
            picture = Picture(base64.b64decode(picture_data))
            
            # Détermine l'extension
            ext = 'jpg' if picture.mime == 'image/jpeg' else 'png'
            
            # Nom du fichier = nom de l'album
            album = audio.tags.get('ALBUM', ['unknown'])[0]
            safe_album = "".join(c for c in album if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            output_path = os.path.join(output_dir, f"{safe_album}.{ext}")
            
            with open(output_path, 'wb') as f:
                f.write(picture.data)
            
            print(f"✓ Cover extraite: {safe_album}.{ext}")
            return True
    except Exception as e:
        print(f"✗ Erreur {file_path}: {e}")
    return False

# Crée le dossier covers
covers_dir = "covers"
os.makedirs(covers_dir, exist_ok=True)

# Parcours tous les sous-dossiers
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.ogg'):
            file_path = os.path.join(root, file)
            extract_cover(file_path, covers_dir)

print("\nTerminé ! Les covers sont dans le dossier 'covers/'")