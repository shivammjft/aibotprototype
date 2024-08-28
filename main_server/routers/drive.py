from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pathlib import Path
import re
import zipfile
import io

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

def download_folder_from_google_drive(folder_id: str, output_dir: Path):
    # Use the Google Drive API to list all files in the folder and download them
    folder_url = f"https://drive.google.com/drive/folders/{folder_id}?usp=sharing"
    
    # Simulate a direct download using a third-party service like gdown or using Google API
    # Here, we use gdown for simplicity
    # You need to install gdown using `pip install gdown`
    
    import gdown
    
    gdown.download_folder(url=folder_url, output=str(output_dir))

@app.post("/download/")
async def download_drive_content(drive_link: str = Form(...)):
    # Extract the ID from the provided Google Drive link
    folder_or_file_id = None
    is_folder = False
    if "drive.google.com" in drive_link:
        if "/folders/" in drive_link:
            folder_or_file_id = drive_link.split("/folders/")[1].split("?")[0]
            is_folder = True
        elif "/d/" in drive_link:
            folder_or_file_id = drive_link.split("/d/")[1].split("/")[0]
        elif "id=" in drive_link:
            folder_or_file_id = drive_link.split("id=")[1].split("&")[0]

    if not folder_or_file_id:
        raise HTTPException(status_code=400, detail="Invalid Google Drive link")

    try:
        if is_folder:
            # Download the entire folder
            download_dir = Path(f"data/{folder_or_file_id}")
            download_dir.mkdir(parents=True, exist_ok=True)
            download_folder_from_google_drive(folder_or_file_id, download_dir)
            return {"message": "Folder downloaded successfully", "download_dir": str(download_dir)}
        else:
            # Download a single file
            file_data, filename = download_file_from_google_drive(folder_or_file_id)
            download_dir = Path(f"data/{folder_or_file_id}")
            download_dir.mkdir(parents=True, exist_ok=True)
            file_path = download_dir / filename
            with open(file_path, "wb") as file:
                file.write(file_data)
            return {"filename": str(file_path), "file_size": len(file_data), "content_type": filename.split('.')[-1]}

    except HTTPException as e:
        print(f"Error: {e.detail}")
        raise e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
