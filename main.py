from fastapi import FastAPIfrom fastapi.responses import HTMLResponseapp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)@app.get("/", response_class=HTMLResponse)async def home():    return """    <html>    <head>        <title>SCN REPLY</title>        <style>            body {                display: flex;                justify-content: center;                align-items: flex-start;                height: 100vh;                background-color: white;                margin: 0;                padding-top: 50px; /* Moves the heading down slightly */            }            h1 {                color: #00008B; /* Dark Blue */                font-size: 3rem;                text-align: center;            }        </style>    </head>    <body>        <h1>SCN REPLY</h1>    </body>    </html>    """