# query-document

Use Adobe AI to read research pdf file pr book.
Do some post processing.
Use langchain to feed it into chat gpt
Ask questions about it!

# Setup

## Adobe API key

1. [Follow instrucitons here](https://developer.adobe.com/document-services/docs/overview/pdf-extract-api/quickstarts/python/)
2. Move your `pdfservices-api-credentials.json` and `private.key` to the folder `ProcessPDF`

## Open AI API Key

1. Sign up for an Open AI account [here](https://openai.com/api/) and login. You should eventually be able to get the key.
2. If not, open [this page](https://platform.openai.com/). Click **Personal** > **View API keys**. Copy the key by clicking **Copy**.
3. Enter your key in `.env.template` and rename it to `.env`

## Install dependencies

```zsh
python -m pip install -r requirements.txt
```

# Run


```zsh
streamlit run main.py
```

# To-Do

Combine scans of multiple PDFs!
