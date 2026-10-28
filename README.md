---
title: First Agent Template
emoji: ⚡
colorFrom: pink
colorTo: yellow
sdk: gradio
sdk_version: 5.23.1
app_file: app.py
pinned: false
tags:
- smolagents
- agent
- smolagent
- tool
- agent-course
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference.

# First Agent Template

A small, interactive AI-agent starter built with [smolagents](https://github.com/huggingface/smolagents) and Gradio. It demonstrates how to connect a language model to Python tools and stream the agent's steps in a chat interface.

The included tools let the agent add two integers and look up the current time in an IANA timezone. The agent's prompt and behavior are configured in `prompts.yaml`; its model provider can be selected with environment variables.

## Features

- Gradio chat interface with streamed agent steps and final answers.
- Local model support through Ollama by default.
- Optional Hugging Face Inference API model support.
- Example tools for integer addition and timezone-aware current time.
- A configurable model and prompt, as a starting point for adding your own tools.

## Requirements

- Python 3.10 or later.
- Ollama installed and running for the default local model setup, or a Hugging Face account/token for the hosted model option.

## Setup

Clone the GitHub repository and enter its directory (replace the placeholders with your repository details). If you already have a local checkout, start from that directory:

```sh
git clone https://github.com/<OWNER>/<REPOSITORY>.git
cd <REPOSITORY>
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run with Ollama (default)

Install [Ollama](https://ollama.com/) and make sure its service is running. Download the default model:

```sh
ollama pull llama:latest
```

Start the app from the repository root:

```sh
python app.py
```

The app connects to Ollama's OpenAI-compatible local API at `http://localhost:11434/v1`. Despite the API compatibility URL, this configuration uses Ollama locally; it does not call OpenAI.

To use a different Ollama model, download it and set its name when launching the app. For example:

```sh
ollama pull qwen2.5-coder:7b
OLLAMA_MODEL=qwen2.5-coder:7b python app.py
```

## Run with Hugging Face

Set up Hugging Face authentication for your environment (for example, with `hf auth login` or the `HF_TOKEN` environment variable), then launch the app with:

```sh
MODEL_PROVIDER=hf python app.py
```

The default hosted model is `Qwen/Qwen2.5-Coder-32B-Instruct`. To select another model, set `HF_MODEL`:

```sh
MODEL_PROVIDER=hf HF_MODEL=your-org/your-model python app.py
```

In Windows PowerShell, set environment variables before running the app:

```powershell
$env:MODEL_PROVIDER = "hf"
python app.py
```

## What to expect

When startup succeeds, Gradio prints a local address (usually `http://127.0.0.1:7860`) and a share URL in the terminal. Open the local address to use the chat UI. Enter a request and submit it; the interface streams the agent's reasoning/action steps, tool execution details, and final answer. Startup and debug logs are also printed in the terminal.

The app currently enables Gradio's `share=True` option, so it creates a shareable public URL as well as a local URL. Anyone with the share URL may be able to access the running interface; do not enter sensitive information, and stop the app when it is no longer needed.

Example requests:

- `What is 23 + 19?`
- `What time is it in Asia/Kolkata?`

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `MODEL_PROVIDER` | `ollama` | Model backend: `ollama` or `hf`. |
| `OLLAMA_MODEL` | `llama:latest` | Ollama model name. Pull the model with `ollama pull` before using it. |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama's OpenAI-compatible API URL. |
| `HF_MODEL` | `Qwen/Qwen2.5-Coder-32B-Instruct` | Model ID used when `MODEL_PROVIDER=hf`. |
| `HF_TOKEN` | — | Optional environment variable for Hugging Face authentication when required by the selected model/account. |

## Troubleshooting

- **Ollama connection error:** Confirm Ollama is installed and running, and that `OLLAMA_BASE_URL` points to its API.
- **Model not found:** Pull the configured model with `ollama pull <model-name>` and ensure `OLLAMA_MODEL` matches it.
- **Hugging Face authentication/model access error:** Log in with the Hugging Face CLI or set `HF_TOKEN`, and confirm your account can access the selected model.
- **Unsupported provider:** `MODEL_PROVIDER` accepts only `ollama` or `hf`.

## Customize

Add tools to `app.py` and include them in the `CodeAgent`'s `tools` list. Keep the final-answer tool in that list, and update `prompts.yaml` if the agent needs additional instructions about when or how to use a tool.
