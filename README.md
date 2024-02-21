# LlamaIndex documentation:

https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html

# Setup:

## 1. Create and source virtual environment within vallis project directory <br>

`python -m venv venv` <br>
`source venv/bin/activate` (anytime you want to activate virtual environment) <br>

## 2. Make sure you are using pip version 24, python version 3.8.11

`pip -V` <br>
`python -V` <br>

## 3. Install all dependencies

`pip install -r requirements.txt` <br>

## 4. Export environment variable `OPENAI_API_KEY` and `REPLICATE_API_TOKEN` (Ask Vaibhav)

### For zsh

`echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc` <br>
`source ~/.zshrc`

### For bash

`echo "export OPENAI_API_KEY='yourkey'" >> ~/.bash_profile` <br>
`source ~/.bash_profile`

<br>

Confirm you have successfully added your API key with `echo $OPENAI_API_KEY`

## 5. Setting up redis for caching (Only important for building index):

`pip install redis` <br> <br>
Make sure docker desktop is opened and create a new container with the following command: <br>
`docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest` <br> <br>
The first time you build the index it will take a lot of time (mostly due to preprocessing of nodes). Subsequent calls will use the redis cache <br>

## 6. Building the index:

`cd index` <br>
`python3 build_index.py` <br>

## 7. Running entire pipeline (used for testing on command line)

`cd src` <br>
`python3 main.py` <br>

## 8. Running entire pipeline (used for testing on local development server)

`python3 main.py` <br>
