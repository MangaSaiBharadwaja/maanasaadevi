import os
from PIL import Image
from pathlib import Path

def crop_to_square(image_path, output_path=None, method='center'):
    """
    Crop an image to square format.
    
    Args:
        image_path: Path to the input image
        output_path: Path to save cropped image (if None, overwrites original)
        method: 'center' for center crop, 'top' for top-aligned crop
    """
    img = Image.open(image_path)
    width, height = img.size
    
    # Determine the size of the square (minimum dimension)
    square_size = min(width, height)
    
    if method == 'center':
        # Calculate center crop coordinates
        left = (width - square_size) // 2
        top = (height - square_size) // 2
        right = left + square_size
        bottom = top + square_size
    elif method == 'top':
        # Top-aligned crop
        left = (width - square_size) // 2
        top = 0
        right = left + square_size
        bottom = square_size
    
    # Crop the image
    cropped_img = img.crop((left, top, right, bottom))
    
    # Save the cropped image
    save_path = output_path if output_path else image_path
    cropped_img.save(save_path, quality=95)
    
    return cropped_img

def crop_images_in_folder(folder_path, output_folder=None, method='center', extensions=None):
    """
    Crop all images in a folder to square format.
    
    Args:
        folder_path: Path to folder containing images
        output_folder: Path to save cropped images (if None, creates 'cropped' subfolder)
        method: 'center' or 'top' crop method
        extensions: List of image extensions to process (default: common image formats)
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    
    # Convert to Path object
    folder_path = Path(folder_path)
    
    # Create output folder if specified, otherwise use 'cropped' subfolder
    if output_folder is None:
        output_folder = folder_path / 'cropped'
    else:
        output_folder = Path(output_folder)
    
    output_folder.mkdir(exist_ok=True)
    
    # Process all images in the folder
    processed_count = 0
    for file_path in folder_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            try:
                output_path = output_folder / file_path.name
                crop_to_square(str(file_path), str(output_path), method=method)
                print(f"✓ Cropped: {file_path.name}")
                processed_count += 1
            except Exception as e:
                print(f"✗ Error processing {file_path.name}: {e}")
    
    print(f"\nProcessed {processed_count} images")
    print(f"Cropped images saved to: {output_folder}")

# Example usage
if __name__ == "__main__":
    # Option 1: Specify folder path directly
    folder_path = r"D:\Abhi\D and D\maanasa_devi\maanasaadevi\static\images"  # Change this to your folder path
    crop_images_in_folder(folder_path, method='center')
    
    # Option 2: Use command line argument
    # import sys
    # if len(sys.argv) > 1:
    #     folder_path = sys.argv[1]
    #     crop_images_in_folder(folder_path, method='center')
    # else:
    #     print("Usage: python crop_images.py <folder_path>")