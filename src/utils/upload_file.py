import os
from fastapi import UploadFile


async def save_file(file : UploadFile):

    try:
        upload_dir = "uploads"
        os.makedirs(upload_dir , exist_ok=True)

        file_path = os.path.join(upload_dir , file.filename)

        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return file_path
    except Exception as e:
        return {"error": str(e)}
    finally:
        file.file.close()



    
    