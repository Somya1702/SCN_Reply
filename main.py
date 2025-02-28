from fastapi import FastAPI, UploadFile, Filefrom fastapi.responses import HTMLResponseapp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)@app.get("/", response_class=HTMLResponse)async def home():    return """    <html>    <head>        <title>SCN REPLY</title>        <style>            body {                display: flex;                flex-direction: column;                justify-content: center;                align-items: center;                height: 100vh;                background-color: white;                margin: 0;                padding-top: 50px;            }            h1 {                color: #00008B;                font-size: 3rem;                text-align: center;            }            button {                background-color: #00008B;                color: white;                padding: 10px 20px;                font-size: 16px;                border: none;                cursor: pointer;                margin-top: 20px;                border-radius: 5px;            }            input {                margin-top: 10px;            }        </style>    </head>    <body>        <h1>SCN REPLY</h1>        <form action="/upload/" method="post" enctype="multipart/form-data">            <input type="file" name="file" accept=".pdf" required>            <button type="submit">Upload</button>        </form>    </body>    </html>    """@app.post("/upload/")async def upload_file(file: UploadFile = File(...)):    return {"filename": file.filename, "content_type": file.content_type}