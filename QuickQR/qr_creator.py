# -*- coding: utf-8  -*-
# @Author  : Yu Ching San 
# @Email   : zhgyqc@163.com
# @Time    : 2023/12/7 20:55
# @File    : qr_creator.py.py
# @Software: PyCharm
import qrcode


def generate_qrcode(data, filename):
    """
    Generate a QR code with the given data and save it as an image.

    Args:
        data (str): The data to be encoded in the QR code.
        filename (str): The filename for the saved QR code image.
    """
    print(f"Generating QR code for data: {data}")
    # Configure QR code parameters
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)
    # Create the QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    print("QR code image generated.")
    # Save the QR code image
    output_path = f"./output/{filename}.png"
    qr_img.save(output_path)
    print(f"QR code image saved at: {output_path}")


if __name__ == '__main__':
    # Example usage with an image URL
    image_url = "https://img-blog.csdnimg.cn/direct/c348769ba0254417b28ca8b4b15a16ec.jpeg"
    print(f"Loading image from URL: {image_url}")
    generate_qrcode(image_url, "test_qrcode")
