# 🌌 CosmicQuery

**AI-powered research assistant using Wikipedia & Web Search**

CosmicQuery is a comprehensive research tool that combines the power of AI with multiple data sources to provide detailed, structured research on any topic. Built with Streamlit and powered by Groq's LLM, it delivers professional research summaries with proper source attribution.

## ✨ Features

- **Dual Data Sources**: Combines Wikipedia content with web search results for comprehensive coverage
- **AI-Powered Analysis**: Uses Groq's Llama 3.1 8B model for intelligent content synthesis
- **Structured Output**: Provides organized summaries with clear sections and source tracking
- **Professional Interface**: Clean, intuitive Streamlit web interface
- **Export Functionality**: Save research results to text files
- **Source Attribution**: Tracks and displays all sources used in research
- **Tool Transparency**: Shows which research methods were employed

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cosmicquery
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file and add your Groq API key
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Getting a Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## 📁 Project Structure

```
cosmicquery/
├── app.py              # Main Streamlit application
├── main.py             # Command-line interface
├── schemas.py          # Pydantic data models
├── tools.py            # Research tools (Wikipedia, Web Search, File Save)
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── README.md          # Project documentation
└── venv/              # Virtual environment (created during setup)
```

## 🛠️ Usage

### Web Interface

1. Start the application: `streamlit run app.py`
2. Open your browser to `http://localhost:8501`
3. Enter your research topic in the input field
4. Click "🚀 Start Research"
5. View comprehensive results with sources
6. Optionally save results to file

### Command Line Interface

```bash
python main.py
```

Enter your research topic when prompted and view results in the terminal.

### Example Topics

- "Quantum Computing Applications"
- "Climate Change Impact on Arctic"
- "Artificial Intelligence in Healthcare"
- "Renewable Energy Technologies"
- "Space Exploration History"

## 🔍 How It Works

1. **Input Processing**: User enters a research topic
2. **Data Collection**: 
   - Wikipedia API fetches relevant articles (top 3 results, 4000 chars max)
   - DuckDuckGo search retrieves current web information
3. **AI Analysis**: Groq's Llama 3.1 processes combined data sources
4. **Structured Output**: Results formatted as JSON with:
   - Topic name
   - Detailed summary (500+ words)
   - Source list
   - Tools used
5. **Presentation**: Clean, organized display in web interface

## 📊 Output Format

Each research result includes:

- **Topic**: Refined topic name
- **Summary**: Comprehensive analysis (minimum 500 words)
- **Sources**: List of all referenced materials
- **Tools Used**: Research methods employed

## 🔧 Technical Details

### Dependencies

- **Streamlit**: Web interface framework
- **LangChain**: LLM orchestration and tooling
- **Groq**: Fast LLM inference
- **Pydantic**: Data validation and parsing
- **DuckDuckGo Search**: Web search functionality
- **Wikipedia API**: Encyclopedia content access

### AI Model

- **Model**: Llama 3.1 8B Instant
- **Provider**: Groq
- **Temperature**: 0.4 (balanced creativity/accuracy)
- **Output**: Structured JSON format

## 🚀 Deployment

### Local Development

```bash
streamlit run app.py
```

### Production Deployment

The app can be deployed on:

- **Streamlit Cloud**: Connect your GitHub repository
- **Heroku**: Use the provided requirements.txt
- **Docker**: Create a Dockerfile for containerization
- **AWS/GCP/Azure**: Deploy as a web service

### Environment Variables for Production

Ensure these are set in your deployment environment:
- `GROQ_API_KEY`: Your Groq API key

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**"streamlit command not found"**
- Ensure virtual environment is activated
- Reinstall streamlit: `pip install streamlit`

**"API key not found"**
- Check `.env` file exists and contains `GROQ_API_KEY`
- Verify API key is valid and active

**"Module not found" errors**
- Run `pip install -r requirements.txt`
- Ensure virtual environment is activated

**Research results not displaying**
- Check internet connection for web search
- Verify Groq API key has sufficient credits
- Try a different research topic

### Performance Tips

- Use specific, focused research topics for better results
- Shorter topics generally process faster
- Check Groq API rate limits if experiencing delays

## 📞 Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**Built with ❤️ using Streamlit, LangChain, and Groq**