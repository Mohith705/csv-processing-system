import requests
from PIL import Image
from io import BytesIO

def download_and_compress_image(image_url, output_path, quality):
    try:
        response = requests.get(image_url)
        response.raise_for_status() 

        image = Image.open(BytesIO(response.content))

        image.save(output_path, format='JPEG', quality=quality)

        print(f"Image downloaded and compressed successfully. Saved to {output_path}")

        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the image: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
