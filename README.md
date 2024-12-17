# FlowAgenda
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Switch Language
- [English README](README.md)
- [中文 README](README.zh.md)

FlowAgenda is a web interface simple, intuitive app that leverages natural language processing (NLP) to allow users to create events by entering plain text descriptions and export them to popular calendars such as Apple Calendar and Google calendar etc. By parsing natural language inputs, FlowAgenda extracts event details such as the title, date, time, and location, and displays them as clean, easy-to-read cards. 

## Features
- **Web Interface**: Access FlowAgenda from any device with a web browser, no installation required.
- **Natural Language Input**: Enter events in natural language, like "Lunch with Sarah next Friday at noon."
- **Automatic Parsing**: FlowAgenda uses a large language model to automatically extract event information.
- **Interactive Card Display**: Events are broken down into individual information cards, each focused on a specific detail:
  - Time card: Date and duration of the event
  - People card: Attendees and participants
  - Location card: Venue and address information
  - Venue card: Specific room or area details
  - Memo card: Additional notes and requirements
  Each card can be individually reviewed and edited, allowing users to verify and modify LLM-extracted information.
- **Export to Calendar**: Currently not supported.
- **Export to .ics file**: Download the event as an .ics file to import into your favorite calendar app by clicking the .ics files.

## Installation

### MacOS and Linux

1. **Clone the Repository**
   ```bash
   git clone "https://github.com/KiwiGaze/FlowAgenda.git"
   cd FlowAgendaPublic
   ```

2. **Install Dependencies for Backend**
   Open a the backend folder in a terminal and run the following command:
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up .env File**
   Create a new file named `.env` in the `backend` folder and add the following environment variables:
   ```bash
    OPENAI_API_KEY=""

    OPENAI_MODEL=""

    GOOGLE_API_KEY=""

    GOOGLE_MODEL=""

    DEEPSEEK_API_KEY=""

    DEEPSEEK_MODEL=""
   
    # Not suggested to use the following model.
    ALIBABA_API_KEY=""

    ALIBABA_MODEL="" # Go to "https://help.aliyun.com/zh/model-studio/getting-started/models#9f8890ce29g5u"for reference

    LLM_PROVIDER="" # Choose from "openai","google","deepseek","alibaba"

    OLLAMA_BASE_URL="http://localhost:11434"

    OLLAMA_MODEL="" # choose according to your local model, llama3.2:1b is suggested.
   ```
4. **Run the Backend**
   ```bash
   python manage.py runserver
   ```
5. **Install Dependencies for Frontend**
   Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   npm install
   ```
6. **Run the Frontend**
   ```bash
    npm run dev
    ```

### Windows

1. **Clone the Repository**
   ```powershell
   git clone "https://github.com/KiwiGaze/FlowAgendaPublic.git"
   cd FlowAgendaPublic
   ```

2. **Install Dependencies for Backend**
   Open Command Prompt or PowerShell in the backend folder and run:
   ```powershell
   cd backend
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
   > Note: If you get a security error in PowerShell, you may need to run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

3. **Set up .env File**
   Create a new file named `.env` in the `backend` folder and add these environment variables:
   ```bash
      OPENAI_API_KEY=""

      OPENAI_MODEL=""

      GOOGLE_API_KEY=""

      GOOGLE_MODEL=""

      DEEPSEEP_API_KEY=""

      DEEPSEEk_MODEL=""

      ALIBABA_API_KEY=""

      ALIBABA_MODEL=""  # Go to "https://help.aliyun.com/zh/model-studio/getting-started/models#9f8890ce29g5u"for reference

      LLM_PROVIDER="" # Choose from "openai","google","deepseek","alibaba" 

      OLLAMA_BASE_URL="http://localhost:11434"

      OLLAMA_MODEL="" # choose according to your local model
   ```
   > Note: You can create this file by running `type nul > .env` in Command Prompt or `New-Item -Path ".env" -ItemType "file"` in PowerShell

4. **Run the Backend**
   With the virtual environment activated, run:
   ```powershell
   python manage.py runserver
   ```

5. **Install Dependencies for Frontend**
   Open a new Command Prompt or PowerShell window and navigate to the frontend folder:
   ```powershell
   cd frontend
   npm install
   ```

6. **Run the Frontend**
   ```powershell
   npm run dev
   ```

> Important Windows-specific notes:
> - Use backslashes (`\`) instead of forward slashes (`/`) for file paths
> - PowerShell commands may differ slightly from Command Prompt
> - Make sure Python and Node.js are added to your system's PATH
> - If using `python` command doesn't work, try `py` instead
> - If you encounter permission issues, try running PowerShell as administrator

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License 

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.