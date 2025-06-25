from PIL import Image
import os

def resize_and_add_border(image, target_size, border_size):
    resized_image = Image.new("RGB", target_size, "black")
    resized_image.paste(image, ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2))
    return resized_image

def load_images():
    number_of_images = 6
    images_loaded = []
    image_files = os.listdir("output/images/imagesWithText")

    # Sort filenames by panel index (assumes filenames like panel_0.png)
    sorted_files = sorted(
        image_files,
        key=lambda name: int("".join(filter(str.isdigit, name)))
    )

    for i in range(number_of_images):
        image_path = os.path.join("output/images/imagesWithText", sorted_files[i])
        image = Image.open(image_path)
        images_loaded.append(image)

    return images_loaded


def main():
    # Desired grid size
    images = load_images()
    len(images)
    columns, rows = 2, 3

    # Calculate the size of the output image
    output_width = columns * images[0].width + (columns - 1) * 10  # 10 is the black border width
    output_height = rows * images[0].height + (rows - 1) * 10  # 10 is the black border width

    # Create a new image with the calculated size
    result_image = Image.new("RGB", (output_width, output_height), "black")

    # Combine images into a grid with black borders
    for i, img in enumerate(images):
        x = (i % columns) * (img.width + 10)  # 10 is the black border width
        y = (i // columns) * (img.height + 10)  # 10 is the black border width

        resized_img = resize_and_add_border(img, (images[0].width, images[0].height), 10)
        result_image.paste(resized_img, (x, y))

    result_image.resize((1024, 1536))
    result_image.save("comic.jpg")

if __name__ == "__main__":
    main()