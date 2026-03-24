import os
import glob
from src.converter import convert_to_sketch
from src.visualizer import save_comparison_figure, save_intensity_graph


def main():
    # 1. Setup project paths
    input_folder = 'data/input'
    output_folder = 'data/output'

    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # 2. Automatically find any image format (jpg, jpeg, png, webp)
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp', '*.JPG', '*.PNG']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))

    # 3. Check if any image exists
    if not image_files:
        print(f"Error: No images found in '{input_folder}'.")
        print("Please drop a .jpg, .png, or .webp file into that folder.")
        return

    # Process the first image found
    input_path = image_files[0]
    filename = os.path.basename(input_path)

    print(f"--- Processing: {filename} ---")

    # 4. Process the image (Converter)
    images, status = convert_to_sketch(input_path)

    if status == "Success":
        # 5. Generate and save Figure
        fig_name = f"figure_{os.path.splitext(filename)[0]}.png"
        figure_path = os.path.join(output_folder, fig_name)
        save_comparison_figure(images, figure_path)

        # 6. Generate and save Graph
        graph_name = f"graph_{os.path.splitext(filename)[0]}.png"
        graph_path = os.path.join(output_folder, graph_name)
        save_intensity_graph(images[-1], graph_path)

        print(f"Done! Results saved in '{output_folder}' as:")
        print(f" - {fig_name}")
        print(f" - {graph_name}")
    else:
        print(f"Error: {status}")


if __name__ == "__main__":
    main()