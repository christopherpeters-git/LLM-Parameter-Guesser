# LLM Parameter Guessing Game

> An interactive CLI game to build intuition for Large Language Model sampling parameters by guessing them from generated output.

It's a small Python project that turns LLM generation parameters into a guessing game.  
Each round, the model responds to a prompt using hidden parameters, and the player must infer those parameters by reading the output.
Right now it only supports OpenAI Platform. Also, only `temperature` and `top_p` can be guessed, since it uses the newer Responses API which does not allow setting parameters like `frequency penalty` or `presence penalty`.

The input can be provided either via text or via voice input. The voice input is currently only supported with Google STT.

This project is designed as an **educational experiment** of working with the OpenAI API and LLM parameters in general.

---

## Install
With `uv` and project as working directory:
- Copy `.env_template` as `.env` and insert your OpenAPI token
- `$ uv sync`
- `$ uv run main.py`

### Requirements
Runs with:
- Python **3.12**
- look at pyproject.toml for pip dependencies

Also needs:
- An OpenAI API key
- Google gcloud setup

