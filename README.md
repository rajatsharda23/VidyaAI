# VidyaAI
A teaching assistant that teaches using the Socratic teaching method.

## Installation Guide (For Developers Only)

This project uses NVIDIA's Nemo Guardrails. 

- **Documentation**: [NVIDIA NeMo Guardrails GitHub](https://github.com/NVIDIA/NeMo-Guardrails)
- **Newer Documentation**: [NVIDIA NeMo Guardrails Documentation](https://docs.nvidia.com/nemo/guardrails/index.html)

Nemo Guardrails works with Python versions 3.9 to 3.11, with the preferred/tested version being 3.10.9.

### Prerequisites

- Python 3.10.9 (recommended)
- Access to the secrets folder (request from project owners)

### Setting Up a Virtual Environment

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. Install the dependencies:
   ```bash
   cd Vidya_LLM
   pip install -r requirements.txt
   ```

## Launching the CLI and Server

1. **Set Up Environment Variables**: Ensure you have your Google Cloud credentials set up. You can do this by creating a `.env` file in the root directory with the following content:
   ```plaintext
   export GOOGLE_APPLICATION_CREDENTIALS="../secrets/pvtKey.json"
   ```

2. **Run the Application**: Start the application using the following command for debugging:
   ```bash
   python g_rail.py
   ```

   To use the service in CLI, run:
   ```bash
   nemoguardrails chat
   ```

   To launch the Nemo Guardrails server, use:
   ```bash
   nemoguardrails server [--config PATH/TO/CONFIGS] [--port PORT] [--prefix PREFIX] [--disable-chat-ui] [--auto-reload] [--default-config-id DEFAULT_CONFIG_ID]
   eg-> nemoguardrails server --config=config --port=7080 --auto-reload
   for deployement -> nemoguardrails server --config=config --port=7080 --disable-chat-ui
   ```

3. **Interact with the Bot**: Once the server is running, you can interact with the bot through the command line interface. Type your questions, and the bot will respond based on its training.

4. **Stopping the Application**: To stop the application, you can simply type `mischief managed` or use `Ctrl + C` in the terminal.

## Additional Information

For more detailed information on how to customize and extend the functionality of VidyaAI, refer to the official [NVIDIA NeMo Guardrails Documentation](https://docs.nvidia.com/nemo/guardrails/index.html).

Feel free to contribute to the project by submitting issues or pull requests on the GitHub repository.
