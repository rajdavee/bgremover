import os
import uuid
from flask import Flask, request, send_file
from io import BytesIO
from rembg import remove
from PIL import Image

app = Flask(__name__)
@app.route("/remove-background/", methods=["POST"])
def remove_background():
    # Check if the request contains a file
    if "file" not in request.files:
        print("No file have submitted")  # Add print for debugging
        return "No file part", 400

    file = request.files["file"]
    
    if file.filename == "":
        print("No selected file")  # Add print for debugging
        return "No selected file", 400

    # Read the uploaded image file
    image_bytes = file.read()

    # Remove the background using rembg
    result = remove(image_bytes)

    # Convert result into a Pillow Image
    image = Image.open(BytesIO(result)).convert("RGBA")

    # Save the result as PNG to be sent as a response
    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # Generate a unique filename for the result
    filename = f"{uuid.uuid4()}.png"

    # Return the image as a stream for download
    return send_file(output, as_attachment=True, download_name=filename, mimetype="image/png")


if __name__ == "__main__":
    # Bind to the PORT environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
