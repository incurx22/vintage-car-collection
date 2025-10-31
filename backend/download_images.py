"""
Download placeholder vintage car images from a free image service.
This script helps set up initial images for development.
"""
import os
import requests
from urllib.parse import quote

# Ensure the images directory exists
IMAGES_DIR = os.path.join('static', 'images')
os.makedirs(IMAGES_DIR, exist_ok=True)

# List of cars and their search terms
CARS = {
    'db5.jpg': 'vintage aston martin db5 silver',
    'belair.jpg': 'vintage 1957 chevrolet bel air',
    'challenger.jpg': '1970 dodge challenger rt',
    'etype.jpg': 'vintage jaguar e-type series 1',
    'camaro.jpg': '1969 chevrolet camaro ss',
    'porsche.jpg': '1973 porsche 911 carrera rs'
}

def download_image(filename, search_term):
    """Download a placeholder image from a free image service."""
    # Using a free placeholder service (replace with your preferred service)
    size = '800x600'
    url = f'https://placehold.co/{size}?text={quote(search_term)}'
    
    filepath = os.path.join(IMAGES_DIR, filename)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f'Downloaded {filename}')
            return True
    except Exception as e:
        print(f'Error downloading {filename}: {e}')
    return False

def main():
    """Download all car images."""
    print('Downloading car images...')
    success = 0
    for filename, search_term in CARS.items():
        if download_image(filename, search_term):
            success += 1
    print(f'Downloaded {success} of {len(CARS)} images')

if __name__ == '__main__':
    main()