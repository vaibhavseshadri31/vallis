
# LlamaIndex documentation:

https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html

# Setup:

## 1. Create and source virtual environment within helios project directory <br>

`python -m venv venv` <br>
`source venv/bin/activate` (anytime you want to activate virtual environment) <br>

## 2. Install LlamaIndex within virtual environment

`pip install llama-index`

## 3. Export environment variable `OPENAI_API_KEY` (store most recent key in API_key.txt)

### For zsh

`echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc` <br> 
`source ~/.zshrc`

### For bash

`echo "export OPENAI_API_KEY='yourkey'" >> ~/.bash_profile` <br>
`source ~/.bash_profile`

<br>

Confirm you have successfully added your API key with `echo $OPENAI_API_KEY`

## 4. Running code

`cd src` <br>
`python3 main.py` <br>

