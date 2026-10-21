# Kubernetes AI Troubleshooting Agent

An AI-powered DevOps assistant built using Python, LangChain, Ollama, and the Kubernetes Python client. This project aims to simplify Kubernetes troubleshooting by allowing users to ask questions in natural language and retrieve relevant cluster information through tools.

**Project status:** In development

## Overview

Troubleshooting Kubernetes workloads often requires checking pod status, reviewing logs, inspecting cluster events, and identifying potential causes of failures.

This project uses a locally running Large Language Model (LLM) to interpret user questions and select appropriate Kubernetes tools to gather information and provide troubleshooting guidance.

## Features

- Natural-language interaction with an AI agent.
- Local LLM integration using Ollama and Llama 3.2.
- Kubernetes node and pod information retrieval.
- Pod log inspection.
- Kubernetes event retrieval.
- Initial troubleshooting support for pod failures, including `CrashLoopBackOff`.
- Python-based implementation using LangChain tools.

*Feature availability depends on the tools currently implemented and tested in the project.*

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | AI agent and tool orchestration |
| Ollama | Local LLM runtime |
| Llama 3.2 | Language model |
| Kubernetes Python client | Kubernetes API interaction |
| kubectl | Cluster access and verification |

## Project Structure

```text
k8s-ai-agent/
├── main.py
├── tools.py
├── test_tools.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

*Note: The Docker-related files are present for future use. The current setup focuses on running the agent locally. Adjust `main.py` to `agent.py` if that is your actual entry-point filename.*

## Prerequisites

- Python installed
- Git installed
- Ollama installed
- Llama 3.2 model downloaded
- `kubectl` installed
- Access to a configured Kubernetes cluster

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/k8s-ai-agent.git
cd k8s-ai-agent
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Set up Ollama

Download the Llama 3.2 model:

```powershell
ollama pull llama3.2
```

Verify that the model is available:

```powershell
ollama list
```

Ensure Ollama is running before starting the agent.

### 5. Configure Kubernetes access

Check the active Kubernetes context:

```powershell
kubectl config current-context
```

Verify cluster connectivity:

```powershell
kubectl get nodes
kubectl get pods -A
```

The Kubernetes Python client uses the configured kubeconfig to connect to the cluster. Ensure that the account has the required permissions to retrieve the resources used by the agent.

### 6. Run the agent

If your entry-point file is `main.py`:

```powershell
python main.py
```

If your entry-point file is `agent.py`:

```powershell
python agent.py
```

## Example Usage

After the agent starts, ask questions such as:

```text
How many pods are running?
```

```text
Show me the pods in the default namespace.
```

```text
Check the logs of a failing pod.
```

```text
Why is my pod restarting?
```

The agent can use the available Kubernetes tools to gather information and generate a response. Results depend on cluster connectivity, permissions, and the tools implemented.

Type `exit` to quit the interactive session.

## Current Limitations

- The agent depends on Ollama and the configured local model.
- Kubernetes queries require valid cluster configuration and authentication.
- Troubleshooting accuracy depends on the information returned by Kubernetes tools and the LLM's interpretation.
- The project is still under development and requires additional testing.

## Future Enhancements

- **Docker containerization:** Package the agent and its dependencies into a Docker image.
- **Kubernetes integration:** Improve reliable access to Kubernetes clusters from containerized environments.
- **Enhanced diagnostics:** Expand troubleshooting for pod failures, scheduling issues, and application errors.
- **Improved testing:** Add more automated tests for the agent and Kubernetes tools.
- **Cloud deployment:** Explore deployment options for running the agent in a cloud environment.

## Learning Objectives

This project provides hands-on practice with:

- Python automation for DevOps.
- LLM integration and AI agents.
- LangChain tool calling.
- Kubernetes API interaction.
- Troubleshooting workloads using logs and events.
- Integrating AI into infrastructure operations.

## Disclaimer

This project is intended for learning and experimentation. AI-generated troubleshooting advice should be verified before making changes to a Kubernetes cluster, especially in production environments.

## Author

**Jobin J**

GitHub: https://github.com/KevinJCloud/k8s-ai-agent.git

<img width="552" height="163" alt="image" src="https://github.com/user-attachments/assets/87d950f6-fdd3-4dbe-bbfe-c056561a1559" />

