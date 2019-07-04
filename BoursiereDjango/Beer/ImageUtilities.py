from PIL import Image, ImageOps
import hashlib
import io
import os


class ImageUtilities:

    @staticmethod
    def resize_save_image(image_file_binary, large_width=600, large_height=400):

        image = Image.open(io.BytesIO(image_file_binary))
        width, height = image.size
        if width < large_width and height < large_height:
            raise Exception("The image is too small, the minimum image width and height are %d and %d.\n"
                            "This image is only %d by %d"
                            % (large_height, large_width, height, width))


        file_name = ImageUtilities.hash_file(image_file_binary)
        file_path = os.path.join(os.getcwd(), 'static\\images\\beers\\%s%s')
        file_path_large = file_path % (file_name, '.jpg')
        size = (large_width, large_height)

        fit_and_resized_image = ImageOps.fit(image, size, Image.ANTIALIAS)

        try:
            fit_and_resized_image.save(file_path_large)
        except IOError as e:
            raise Exception("The image could not be saved to the database, please contact the administrator")
        return file_path_large

    @staticmethod
    def hash_file(file_binary):
        hasher = hashlib.md5()
        hasher.update(file_binary)
        return hasher.hexdigest()


# TODO : Verify that the class works properly
