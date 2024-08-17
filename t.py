import barcode
from barcode.writer import ImageWriter
from io import BytesIO
import base64

def generate_barcode(text):
    try:
        print(f"Generating barcode for: {text}")
        ean_class = barcode.get_barcode_class('ean13')
        ean_code = ean_class(text, writer=ImageWriter())
        buffer = BytesIO( )
        ean_code.write(buffer)
        buffer.seek(0)
        barcode_image = buffer.getvalue()
        encoded_image = base64.b64encode(barcode_image).decode('utf-8')
        return encoded_image
    except Exception as e:
        print(f"Error generating barcode for {text}: {e}")
        return None
    
# Test with a sample value
barcode_image = generate_barcode('123456789012')
if barcode_image:
    print(f"Barcode generated successfully: {barcode_image[:50]}...")  # Print the first 50 characters of the encoded image
else:
    print("Failed to generate barcode.")




