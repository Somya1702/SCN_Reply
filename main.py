import osfrom fastapi import FastAPI, UploadFile, Filefrom fastapi.responses import HTMLResponsefrom docx import Documentimport fitz  # PyMuPDFimport openaiapp = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)# Fetch OpenAI API Key from Render Environment VariableOPENAI_API_KEY = os.getenv("OPENAI_API_KEY")@app.get("/", response_class=HTMLResponse)async def home():    return """    <html>    <head>        <title>SCN REPLY</title>        <style>            body {                display: flex;                flex-direction: column;                justify-content: center;                align-items: center;                height: 100vh;                background-color: white;                margin: 0;                padding-top: 50px;            }            h1 {                color: #00008B;                font-size: 3rem;                text-align: center;            }            button {                background-color: #00008B;                color: white;                padding: 10px 20px;                font-size: 16px;                border: none;                cursor: pointer;                margin-top: 20px;                border-radius: 5px;            }            #analysis ol {                text-align: left;                font-size: 18px;                color: black;            }            input {                margin-top: 10px;            }            p {                font-size: 18px;                color: green;            }        </style>    </head>    <body>        <h1>SCN REPLY</h1>        <form id="uploadForm" action="/upload/" method="post" enctype="multipart/form-data">            <input type="file" name="file" accept=".pdf" required>            <button type="submit">Upload</button>        </form>        <p id="message"></p>        <div id="analysis"></div>        <script>            document.querySelector("#uploadForm").onsubmit = async (e) => {                e.preventDefault();                const formData = new FormData(e.target);                document.getElementById("message").innerHTML = "Uploading...";                const response = await fetch("/upload/", {                    method: "POST",                    body: formData                });                const result = await response.json();                document.getElementById("message").innerHTML = "File uploaded successfully!";                let analysisHtml = "<ol>";                result.analysis.forEach((point, index) => {                    analysisHtml += `<li>${point}</li>`;                });                analysisHtml += "</ol>";                document.getElementById("analysis").innerHTML = analysisHtml;            };        </script>    </body>    </html>    """def extract_text_from_pdf(pdf_path):    """ Extract text from PDF using PyMuPDF (fitz). """    doc = fitz.open(pdf_path)    text = ""    for page in doc:        text += page.get_text("text") + "\n"    return textdef analyze_text_with_chatgpt(text):    """ Send extracted text to OpenAI ChatGPT for detailed analysis in numbered format. """    api_key = os.getenv("OPENAI_API_KEY")    if not api_key:        print("Error: OpenAI API key is missing. Please configure it in Render.")        return ["Error: OpenAI API key is missing. Please configure it in Render."]    try:        client = openai.OpenAI(api_key=api_key)        response = client.chat.completions.create(            model="gpt-4",            messages=[                {"role": "system", "content": "You are an AI that analyzes PDFs and provides a detailed report in numbered points."},                {"role": "user", "content": f"Analyze this document and provide a detailed breakdown in numbered points:\n{text}"}            ]        )        # Split response into numbered points        analysis_points = response.choices[0].message.content.split("\n")        analysis_points = [point.strip("- ") for point in analysis_points if point]  # Clean up formatting        return analysis_points    except openai.OpenAIError as e:        print(f"OpenAI API Error: {e}")        return [f"Error: {e}"]@app.post("/upload/")async def upload_file(file: UploadFile = File(...)):    pdf_path = f"temp_{file.filename}"        # Save the uploaded file    with open(pdf_path, "wb") as buffer:        buffer.write(file.file.read())    # Extract text from the PDF    extracted_text = extract_text_from_pdf(pdf_path)    # Send text to ChatGPT for analysis    analysis_result = analyze_text_with_chatgpt(extracted_text)    # Remove the temporary PDF file    os.remove(pdf_path)    return {"analysis": analysis_result}