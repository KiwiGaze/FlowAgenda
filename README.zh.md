# FlowAgenda
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
## 切换语言
- [英文 README](README.md)
- [中文 README](README.zh.md)

`FlowAgenda` 是一个简单、直观的网页界面应用，利用自然语言处理技术 (NLP)，允许用户通过输入普通文本描述来创建事件，并将其导出到常见的日历（如 Apple Calendar 和 Google Calendar 等）。通过解析自然语言输入，`FlowAgenda` 提取事件的详细信息，如标题、日期、时间和地点，并以简洁易读的卡片形式展示。

## 特性
- **网页界面**：可以在任何带有浏览器的设备上访问 `FlowAgenda`，无需安装。
- **自然语言输入**：用自然语言输入事件，例如：“下周五中午和 Sarah 一起吃个午饭。”
- **自动解析**：`FlowAgenda` 使用大型语言模型自动提取事件信息。
- **交互卡片展示**：事件被分解为独立的信息卡片，每张卡片重点注意一个特定细节：
  - 时间卡：事件的日期和持续时间
  - 人员卡：与会者和参与者
  - 地点卡：地点和地址信息
  - 地点卡：特定房间或区域详细信息
  - 备注卡：附加的注释和要求
  每张卡片可以单独查看和编辑，允许用户验证并修改由 LLM 提取的信息。
- **导出到日历**：当前不支持。
- **导出为 .ics 文件**：通过点击 .ics 文件将事件下载为 .ics 文件，以便导入到您喜欢的日历应用中。

## 安装

### MacOS 和 Linux

1. **克隆仓库**
   ```bash
   git clone "https://github.com/KiwiGaze/FlowAgenda.git"
   cd FlowAgendaPublic
   ```

2. **为后端安装依赖**
   打开后端文件夹，在终端中运行：
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **设置 .env 文件**
   在 `backend` 文件夹中创建一个名为 `.env` 的新文件，并添加以下环境变量：
   ```bash
    OPENAI_API_KEY=""

    OPENAI_MODEL=""

    GOOGLE_API_KEY=""

    GOOGLE_MODEL=""

    DEEPSEEK_API_KEY=""

    DEEPSEEK_MODEL=""

    # 不建议使用以下模型。
    ALIBABA_API_KEY=""

    ALIBABA_MODEL=""

    LLM_PROVIDER="" # 可从 "openai","google","deepseek","alibaba" 中选择

    OLLAMA_BASE_URL="http://localhost:11434"

    OLLAMA_MODEL=""
   ```

4. **运行后端**
   ```bash
   python manage.py runserver
   ```

5. **为前端安装依赖**
   打开新终端，并进入 `frontend` 文件夹：
   ```bash
   cd frontend
   npm install
   ```

6. **运行前端**
   ```bash
   npm run dev
   ```

### Windows

1. **克隆仓库**
   ```powershell
   git clone "https://github.com/KiwiGaze/FlowAgendaPublic.git"
   cd FlowAgendaPublic
   ```

2. **为后端安装依赖**
   在后端文件夹中打开 Command Prompt 或 PowerShell，运行：
   ```powershell
   cd backend
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **设置 .env 文件**
   在 `backend` 文件夹中创建一个名为 `.env` 的文件，并添加环境变量。

4. **运行后端**
   ```powershell
   python manage.py runserver
   ```

5. **为前端安装依赖**
   ```powershell
   cd frontend
   npm install
   ```

6. **运行前端**
   ```powershell
   npm run dev
   ```

## 贡献

欢迎贡献！感谢您提交 issue 或 pull request。

## 协议

该项目使用 MIT License 协议。详情请参见 [LICENSE](LICENSE) 文件。
