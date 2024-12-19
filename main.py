import os
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from rembg import remove
from PIL import Image
from fastapi.responses import StreamingResponse
import uuid
import uvicorn

app = FastAPI()

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")  # Debugging line

    # Read the uploaded image file
    image_bytes = await file.read()

    # Remove the background using rembg
    result = remove(image_bytes)

    # Convert result into a Pillow Image
    image = Image.open(BytesIO(result)).convert("RGBA")

    # Save the result as PNG to be sent as a response
    output = BytesIO()
    image.save(output, format="PNG")
    output.seek(0)

    # Return the image as a stream for download
    return StreamingResponse(
        output,
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename={uuid.uuid4()}.png"}
    )

if __name__ == "__main__":
    # Bind to the PORT environment variable or default to 8000
    port = int(os.environ.get("PORT",8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
