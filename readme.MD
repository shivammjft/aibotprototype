CHROMA COMMAND
chroma run --host localhost --port 5000 --path ~/companydb

processing server port : 9000  
command for processing server : uvicorn main:app --host 0.0.0.0 --port 9000 --reload
main server port :8000
command for main server : uvicorn main:app --host 0.0.0.0 --port 8000 --reload
