# PDF to DOI
This tool is designed to help quickly extract DOI data from publication titles cited as references in PDF documents.

## Workflow
The general worklow is as follows:

- Convert PDF to JSON using AXA/Parsr API (https://github.com/axa-group/Parsr)
- Convert JSON to tokenized text using Spacy Tokenizer
- Annotated the text manually using the front end
- Extract DOI data using the Crossref and Unpaywall APIs given the annotated reference titles


## Dependencies
- Enable WSL on Windows [link](https://windowsloop.com/enable-wsl-windows-10-home/#:~:text=Steps%20to%20Enable%20WSL%20on%20Windows%2010%20Home,files%20and%20enables%20the%20feature.%20More%20items...%20)
- Install Docker with WSL back-end [link](https://docs.docker.com/desktop/windows/wsl/)
- Install Python (>=3.7) [link](https://www.python.org/downloads/windows/)
- Install Node.js [link](https://nodejs.org/en/download/)

## First time setup
- Clone project repo
    - Open CMD (Hit WinKey + Write "cmd" + Hit Enter) and paste:

```sh
    cd %userprofile%
    mkdir source
    cd source
    git clone https://github.com/nikitcha/ceebios-pdfdoi.git
```

- Pull docker container
    - Open CMD and paste:

```sh
docker pull axarev/parsr
```

- Create Python virtual environment and install backend dependencies
    - Open CMD and paste:
    
```sh
cd %userprofile%
mkdir envs
cd envs
python -m venv pdfdoi
pdfdoi\Scripts\activate
cd %userprofile%\source\ceebios-pdfdoi\backend
pip install -r requirements.txt
```

- Install Node.js dependencies
    - Open CMD and paste:
```sh
cd %userprofile%\source\ceebios-pdfdoi\frontend
yarn install
```

## Starting the application
- Run Parsr API
    - Open CMD and paste:
    
```sh
docker run -p 3001:3001 axarev/parsr
```

- Run backend
    - Open CMD and paste:

```sh
%userprofile%\envs\pdfdoi\Scripts\activate
cd %userprofile%\source\ceebios-pdfdoi\backend
uvicorn main:app --reload
```

- Run frontend
    - Open CMD and paste:
```sh
cd %userprofile%\source\ceebios-pdfdoi\frontend
npm run start
```


## Usage