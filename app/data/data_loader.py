from app.core.config import settings
import aiohttp
import asyncio
import os
from pathlib import Path

class DataLoader:
    def __init__(self):
        self.data_dir = Path(f"{os.getcwd()}/app/data")
        self.cats_dir = self.data_dir / "cats"
        self.dogs_dir = self.data_dir / "dogs"
        
        # Create directories if they don't exist
        self.cats_dir.mkdir(parents=True, exist_ok=True)
        self.dogs_dir.mkdir(parents=True, exist_ok=True)

    async def fetch_data(self, limit:int=10):
        async with aiohttp.ClientSession() as session:
            # Get cat and dog image metadata
            async with session.get(f"https://api.thecatapi.com/v1/images/search?limit={limit}&breed_ids=beng&api_key={settings.THE_CAT_API_KEY}") as cat_response:
                cat_images = await cat_response.json()
            
            async with session.get(f"https://api.thedogapi.com/v1/images/search?limit={limit}&breed_ids=beng&api_key={settings.THE_DOG_API_KEY}") as dog_response:
                dog_images = await dog_response.json()

            # Extract image URLs
            cat_urls = [img["url"] for img in cat_images]
            dog_urls = [img["url"] for img in dog_images]

            # Fetch image bytes concurrently
            async def fetch_image(url):
                async with session.get(url) as response:
                    return await response.read()

            cat_bytes = await asyncio.gather(*[fetch_image(url) for url in cat_urls])
            dog_bytes = await asyncio.gather(*[fetch_image(url) for url in dog_urls])

            return cat_bytes, dog_bytes

    def save_data(self, cat_bytes, dog_bytes):
        # Save cat images
        for i, img_bytes in enumerate(cat_bytes):
            with open(self.cats_dir / f"cat_{i}.jpg", "wb") as f:
                f.write(img_bytes)
                
        # Save dog images
        for i, img_bytes in enumerate(dog_bytes):
            with open(self.dogs_dir / f"dog_{i}.jpg", "wb") as f:
                f.write(img_bytes)

    def load_data(self):
        """
        Returns paths to all images in the dataset
        """
        cat_paths = list(self.cats_dir.glob("*.jpg"))
        dog_paths = list(self.dogs_dir.glob("*.jpg"))
        return cat_paths, dog_paths

    def clean_data(data):
        pass