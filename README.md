# PDF to DOI
This tool is designed to help quickly extract DOI data from publication titles cited as references in PDF documents.

## Workflow
The general worklow is as follows:

- Convert PDF to JSON using AXA/Parsr API (https://github.com/axa-group/Parsr)
- Convert JSON to tokenized text using Spacy Tokenizer
- Annotated the text manually using the front end
- Extract DOI data using the Crossref and Unpaywall apis given the annotated reference titles


## Dependencies
- Enable WSL on Windows [link](https://windowsloop.com/enable-wsl-windows-10-home/#:~:text=Steps%20to%20Enable%20WSL%20on%20Windows%2010%20Home,files%20and%20enables%20the%20feature.%20More%20items...%20)
- Install Docker with WSL back-end [link](https://docs.docker.com/desktop/windows/wsl/)
- Install Python (>=3.7) [link](https://www.python.org/downloads/windows/)
- Install Node.js [link](https://nodejs.org/en/download/)

## First time setup
- Pull docker container
- Create Python virtual environment and install backend dependencies

## Starting
- Run Parsr API
docker run -p 3001:3001 axarev/parsr

- Run backend
cd backend
uvicorn main:app --reload

- Run front end
cd frontend
npm run startgit
