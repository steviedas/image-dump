import requests
import random
import os

def download_pexels_images(api_key: str, query: str, count: int = 1, download_path: str = './pexels_downloads') -> int:
    """
    Searches Pexels for a query, retrieves 'original' quality URLs, and downloads 
    the specified count of photos to the designated path.

    Args:
        api_key (str): Your Pexels API key.
        query (str): The search term (e.g., 'trains').
        count (int): The number of unique images to attempt to download (max 80).
        download_path (str): The local directory path where images will be saved.

    Returns:
        int: The number of images successfully downloaded.
    """
    per_page = min(count, 80)
    API_URL = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": per_page}
    
    successful_downloads = 0

    try:
        if not os.path.exists(download_path):
            print(f"Creating directory: {download_path}")
            os.makedirs(download_path)
    except OSError as e:
        print(f"Error creating directory {download_path}: {e}")
        return 0

    try:
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        photos = data.get('photos', [])
        
        if not photos:
            print(f"Error: No images found for query '{query}'.")
            return 0

        safe_query = query.replace(' ', '_').lower()
        
        
        print(f"Found {len(photos)} photos. Attempting to download {min(count, len(photos))} to '{download_path}'...")

        for i, photo in enumerate(photos[:count]):
            image_url = photo['src'].get('original')
            
            if not image_url:
                print(f"Skipping photo {i+1}: 'original' size URL not available.")
                continue

            extension = os.path.splitext(image_url.split('?')[0])[-1] or '.jpg'
            base_filename = f"{safe_query}_{i+1:02d}{extension}" 
            
            final_filepath = os.path.join(download_path, base_filename) 

            print(f"Downloading image {i+1}/{min(count, len(photos))} to: {final_filepath}")

            image_response = requests.get(image_url, stream=True)
            image_response.raise_for_status() 

            with open(final_filepath, 'wb') as file:
                for chunk in image_response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            
            successful_downloads += 1

        print(f"\n✨ Batch download complete! Successfully saved {successful_downloads} images in '{download_path}'.")
        return successful_downloads

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return successful_downloads

MY_API_KEY="PY8ut5UMGUPyp3CXVNBHyArCN6VaNyQNvvsFCrFFh7PvzXjfOJC3QAcp"
SEARCH_TERM = "regional train" 

NUM_IMAGES_TO_DOWNLOAD = 100
DOWNLOAD_FOLDER = f"images/{SEARCH_TERM.replace(' ', '_').lower()}"

download_count = download_pexels_images(
    api_key=MY_API_KEY, 
    query=SEARCH_TERM, 
    count=NUM_IMAGES_TO_DOWNLOAD, 
    download_path=DOWNLOAD_FOLDER
)
