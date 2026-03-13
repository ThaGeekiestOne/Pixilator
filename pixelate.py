from PIL import Image

def pixelate_image(image_path, pixel_size):
    

    
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found at: {image_path}")

    img = img.resize((img.width // pixel_size, img.height // pixel_size), Image.NEAREST)
    img = img.resize((img.width * pixel_size, img.height * pixel_size), Image.NEAREST)
    return img

if __name__ == '__main__':
    try:
        pixelated_img = pixelate_image("test_image.jpg", 8) 
        pixelated_img.save("pixelated_test_image.jpg")
        print("Image pixelated successfully! Saved as pixelated_test_image.jpg")
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")
