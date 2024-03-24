import os
import qrcode
import cv2
from pyzbar import pyzbar

class QRCodeManager:
    def __init__(self, media_dir="."):
        """Initialize the QRCodeManager class."""
        self.qr_code = None
        self.media_dir = media_dir

    def create_qr_code(self, data, file_name="qr_code.png", version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4):
        """
        Create a QR code with customizable parameters.

        Args:
        - data (str): The data to encode in the QR code.
        - file_name (str, optional): The name of the file to save the QR code image. Defaults to "qr_code.png".
        - version (int, optional): The QR code version. Defaults to 1.
        - error_correction (int, optional): The error correction level. Defaults to qrcode.constants.ERROR_CORRECT_L.
        - box_size (int, optional): The size of each box in the QR code. Defaults to 10.
        - border (int, optional): The border size of the QR code. Defaults to 4.
        """
        # Initialize the QR code with specified parameters
        self.qr_code = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )
        
        # Add data to the QR code and generate the image
        self.qr_code.add_data(data)
        self.qr_code.make(fit=True)
        
        # Construct the full path for the image file
        file_path = os.path.join(self.media_dir, file_name)
        
        img = self.qr_code.make_image(fill_color="black", back_color="white")
        
        # Save the image
        img.save(file_path)
        print(f"QR code generated and saved as {file_path}")

    def read_qr_code(self, image_path):
        """
        Read a QR code from an image.

        Args:
        - image_path (str): The path to the image containing the QR code.

        Returns:
        - list: A list of dictionaries containing the decoded data and type of each QR code found.
        """
        # Read the image and convert it to grayscale
        full_path = os.path.join(self.media_dir, image_path)
        image = cv2.imread(full_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Decode the QR code
        decoded_objects = pyzbar.decode(gray_image)

        qr_data = []
        for obj in decoded_objects:
            # Decode the data and get the type of the QR code
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type
            qr_data.append({"data": barcode_data, "type": barcode_type})
            
            print(f"Data: {barcode_data}, Type: {barcode_type}")

        return qr_data

    def display_qr_code(self):
        """Display the generated QR code."""
        if self.qr_code:
            img = self.qr_code.make_image(fill_color="black", back_color="white")
            img.show()
        else:
            print("No QR code generated yet.")


if __name__ == "__main__":

    try:
        media_dir = input("Enter media directory path (default is current directory): ") or "."
        qr_manager = QRCodeManager(media_dir)
        while True:
            print("\nQR Code Manager")
            print("1. Create QR Code")
            print("2. Read QR Code")
            print("3. Display QR Code")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == "1":
                data = input("Enter data for QR code: ")
                file_name = input("Enter file name to save QR code (default is qr_code.png): ")
                if not file_name:
                    file_name = "qr_code.png"
                version = int(input("Enter QR code version (default is 1): ") or 1)
                error_correction = input("Enter error correction level (L, M, Q, H - default is L): ").upper() or 'L'
                box_size = int(input("Enter box size (default is 10): ") or 10)
                border = int(input("Enter border size (default is 4): ") or 4)
                
                qr_manager.create_qr_code(data, file_name, version=version, error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{error_correction}"), box_size=box_size, border=border)

            elif choice == "2":
                image_path = input("Enter the path to the QR code image: ")
                qr_manager.read_qr_code(image_path)

            elif choice == "3":
                qr_manager.display_qr_code()

            elif choice == "4":
                break

            else:
                print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass