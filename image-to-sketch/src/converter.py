import cv2


def convert_to_sketch(image_path):
    """
    Transforms an image into a pencil sketch through 4 main stages.
    Returns a list of images [original, grayscale, blurred, sketch].
    """
    # 1. Load the original image
    img = cv2.imread(image_path)
    if img is None:
        return None, "Error: Image not found. Check the path."

    # 2. Convert to Grayscale
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Invert the Gray Image
    inverted_image = 255 - gray_image

    # 4. Apply Gaussian Blur to the inverted image
    # The (21, 21) kernel size controls the sketch's softness
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)

    # 5. Create the Sketch (Dodge Blend)
    # This divides the grayscale image by the inverted blurred image
    inverted_blurred = 255 - blurred
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)

    return [img, gray_image, blurred, pencil_sketch], "Success"
