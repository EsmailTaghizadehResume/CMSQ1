
import qrcode
from PIL import Image, ImageDraw, ImageFont

class QRCodeGenerator:
    def __init__(self, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        self.font_path = font_path

    def create_qr_code(self, data, text):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Prepare to draw on the image
        draw = ImageDraw.Draw(img)
        
        # Load a font
        try:
            font = ImageFont.truetype(self.font_path, 20)
        except IOError:
            font = ImageFont.load_default()
        
        # Position for text (upper left corner)
        text_position = (10, 10)
        
        # Add text to image
        draw.text(text_position, text, fill="black", font=font)
        
        return img

    def save_images(self, images, products):
        # Save each image as PNG
        for i, image in enumerate(images):
            product = products[i]
            image_path = f"{product.name}.png"  # Naming files as qr_code_1.png, qr_code_2.png, etc.
            image.save(image_path)

    def generate_and_save(self, data_text_pairs, products):
        qr_images = []

        # Create the QR codes
        for data, text in data_text_pairs:
            qr_image = self.create_qr_code(data, text)
            qr_images.append(qr_image)

        # Save the QR codes as PNG files
        self.save_images(qr_images, products)
