import matplotlib.pyplot as plt
import cv2


def save_comparison_figure(images, output_path):
    """
    Creates a side-by-side figure showing the conversion stages.
    """
    titles = ['Original', 'Grayscale', 'Blurred', 'Final Sketch']
    plt.figure(figsize=(16, 4))

    for i in range(len(images)):
        plt.subplot(1, 4, i + 1)

        # If it's the original (3 channels), convert BGR to RGB for Matplotlib
        if len(images[i].shape) == 3:
            display_img = cv2.cvtColor(images[i], cv2.COLOR_BGR2RGB)
            plt.imshow(display_img)
        else:
            # Grayscale images need the 'gray' colormap
            plt.imshow(images[i], cmap='gray')

        plt.title(titles[i])
        plt.axis('off')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_intensity_graph(sketch_image, output_path):
    """
    Generates a histogram graph of the sketch's pixel intensity.
    """
    plt.figure(figsize=(10, 5))
    plt.hist(sketch_image.ravel(), bins=256, range=[0, 256], color='gray')
    plt.title('Final Sketch: Pixel Intensity Distribution')
    plt.xlabel('Pixel Value (0=Black, 255=White)')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(output_path)
    plt.close()