import osfrom fastapi import FastAPI, UploadFile, Filefrom fastapi.responses import HTMLResponse, FileResponsefrom docx import Documentimport fitz  # PyMuPDFimport openaiapp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)# Fetch OpenAI API Key from Render Environment VariableOPENAI_API_KEY = os.getenv("OPENAI_API_KEY")@app.get("/", response_class=HTMLResponse)async def home():    return """    <html>    <head>        <title>SCN REPLY</title>        <style>            body {                display: flex;                flex-direction: column;                justify-content: center;                align-items: center;                height: 100vh;                background-color: white;                margin: 0;                padding-top: 50px;            }            h1 {                color: #00008B;                font-size: 3rem;                text-align: center;            }            button {                background-color: #00008B;                color: white;                padding: 10px 20px;                font-size: 16px;                border: none;                cursor: pointer;                margin-top: 20px;                border-radius: 5px;            }            #downloadButton {                display: none;            }            input {                margin-top: 10px;            }            p {                font-size: 18px;                color: green;            }        </style>    </head>    <body>        <h1>SCN REPLY</h1>        <form id="uploadForm" action="/upload/" method="post" enctype="multipart/form-data">            <input type="file" name="file" accept=".pdf" required>            <button type="submit">Upload</button>        </form>        <p id="message"></p>        <button id="downloadButton" onclick="window.location.href='/download/'">Download Word File</button>        <div id="analysis"></div>        <script>            document.querySelector("#uploadForm").onsubmit = async (e) => {                e.preventDefault();                const formData = new FormData(e.target);                const response = await fetch("/upload/", {                    method: "POST",                    body: formData                });                const result = await response.json();                document.getElementById("message").innerHTML = "File uploaded successfully!";                document.getElementById("downloadButton").style.display = "block";                document.getElementById("analysis").innerHTML = "<p><b>AI Analysis:</b> " + result.analysis + "</p>";            };        </script>    </body>    </html>    """def extract_text_from_pdf(pdf_path):    """ Extract text from PDF using PyMuPDF (fitz). """    doc = fitz.open(pdf_path)    text = ""    for page in doc:        text += page.get_text("text") + "\n"    return textdef analyze_text_with_chatgpt(text):    """ Send extracted text to OpenAI ChatGPT for analysis. """    if not OPENAI_API_KEY:        return "Error: OpenAI API key is missing. Please configure it in Render."        openai.api_key = OPENAI_API_KEY    response = openai.ChatCompletion.create(        model="gpt-4",        messages=[            {"role": "system", "content": "You are an AI that analyzes PDFs."},            {"role": "user", "content": f"Analyze this document: {text}"}        ],    )    return response["choices"][0]["message"]["content"]@app.post("/upload/")async def upload_file(file: UploadFile = File(...)):    pdf_path = f"temp_{file.filename}"        # Save the uploaded file    with open(pdf_path, "wb") as buffer:        buffer.write(file.file.read())    # Extract text from the PDF    extracted_text = extract_text_from_pdf(pdf_path)    # Send text to ChatGPT for analysis    analysis_result = analyze_text_with_chatgpt(extracted_text)    # Remove the temporary PDF file    os.remove(pdf_path)    return {"analysis": analysis_result}@app.get("/download/")async def download_file():    doc = Document()    doc.save("Blank_Document.docx")  # Save an empty Word file    return FileResponse("Blank_Document.docx", filename="Blank_Document.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")