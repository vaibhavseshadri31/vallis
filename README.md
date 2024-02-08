# LlamaIndex documentation:

https://docs.llamaindex.ai/en/stable/getting_started/starter_example.html

# Setup:

## 1. Create and source virtual environment within vallis project directory <br>

`python -m venv venv` <br>
`source venv/bin/activate` (anytime you want to activate virtual environment) <br>

## 2. Install LlamaIndex within virtual environment

`pip install llama-index`

## 3. Export environment variable `OPENAI_API_KEY` and `REPLICATE_API_TOKEN` (store most recent key in API_key.txt)

### For zsh

`echo "export OPENAI_API_KEY='yourkey'" >> ~/.zshrc` <br>
`source ~/.zshrc`

### For bash

`echo "export OPENAI_API_KEY='yourkey'" >> ~/.bash_profile` <br>
`source ~/.bash_profile`

<br>

Repeat steps for `REPLICATE_API_TOKEN` <br>
Confirm you have successfully added your API key with `echo $OPENAI_API_KEY` / `echo $REPLICATE_API_TOKEN`

## 4. Setting up redis for caching:

`pip install redis` <br> <br>
Make sure docker desktop is opened and create a new container with the following command: <br>
`docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest` <br> <br>
The first time you build the index it will take a lot of time (mostly due to preprocessing of nodes). Subsequent calls will use the redis cache <br>

## 5. Building the index:

`cd index` <br>
`python3 build_index.py` <br>

## 6. Running entire pipeline

`cd src` <br>
`python3 main.py` <br>
