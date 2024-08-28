from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pathlib import Path
import re

app = FastAPI()

# Allow CORS for local development, adjust origins for production
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",  # If serving frontend from a file on a local machine
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def download_file_from_google_drive(file_id: str) -> (bytes, str):
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)
    
    if response.status_code == 200:
        # Extract the filename from the Content-Disposition header
        content_disposition = response.headers.get('content-disposition')
        filename = None
        if content_disposition:
            # Use regex to extract filename from the header
            match = re.search(r'filename="(.+)"', content_disposition)
            if match:
                filename = match.group(1)
        
        # Fallback to file ID if filename is not found
        if not filename:
            filename = file_id
        
        return response.content, filename
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to download file")

@app.post("/download/")
async def download_drive_file(drive_link: str = Form(...)):
    # Extract the file ID from the provided Google Drive link
    file_id = None
    if "drive.google.com" in drive_link:
        if "/d/" in drive_link:
            file_id = drive_link.split("/d/")[1].split("/")[0]
        elif "id=" in drive_link:
            file_id = drive_link.split("id=")[1].split("&")[0]

    if not file_id:
        raise HTTPException(status_code=400, detail="Invalid Google Drive link")

    try:
        # Download the file
        file_data, filename = download_file_from_google_drive(file_id)
        print(f"Downloaded {len(file_data)} bytes with filename {filename}.")

        # Create a directory for the file using the file_id
        download_dir = Path(f"data/{file_id}")
        download_dir.mkdir(parents=True, exist_ok=True)
        print(f"Directory created at: {download_dir}")

        # Save the file to the created directory with the original name
        file_path = download_dir / filename
        with open(file_path, "wb") as file:
            file.write(file_data)
        print(f"File saved at: {file_path}")

        return {"filename": str(file_path), "file_size": len(file_data), "content_type": filename.split('.')[-1]}
    except HTTPException as e:
        print(f"Error: {e.detail}")
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
