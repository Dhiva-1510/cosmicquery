import json
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from schemas import ResearchResponse
from tools import search_tool, wiki_tool, save_tool

# ------------------------
# Setup
# ------------------------
load_dotenv()

st.set_page_config(
    page_title="CosmicQuery",
    page_icon="images/logo.jpg",
    layout="centered"
)

# ------------------------
# Header
# ------------------------

st.markdown(
    """
    <div style="text-align:center; margin-bottom:2rem;">
        <h1 style="font-size:3rem; margin:0.5rem 0; color:rgb(46, 134, 171);">
            CosmicQuery
        </h1>
        <p style="font-size:1.1rem; color:#5A6C7D;">
            AI-powered research assistant using Wikipedia & Web Search
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()

# ------------------------
# LLM + Parser
# ------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    max_tokens=4000
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional research assistant. Create comprehensive, detailed research summaries.

REQUIREMENTS:
- Write detailed summaries of 2000+ words
- Follow the exact 8-section structure provided
- Use all available research material
- Output ONLY a valid JSON object with these exact fields: topic, summary, sources, tools_used
- Do NOT include schema, properties, or any other JSON structure
- Do NOT include any text outside the JSON object

STRUCTURE for summary field (write as continuous text with clear section headers):
1. **Introduction and Definition** (300+ words)
2. **Historical Background and Development** (350+ words) 
3. **Current State and Recent Developments** (300+ words)
4. **Key Concepts and Mechanisms** (400+ words)
5. **Applications and Real-World Examples** (350+ words)
6. **Challenges and Limitations** (300+ words)
7. **Future Prospects and Implications** (300+ words)
8. **Conclusion** (200+ words)

Example format (replace with actual content):
{{
  "topic": "Your Topic Name Here",
  "summary": "**Introduction and Definition**\\n\\nYour 300+ word introduction here...\\n\\n**Historical Background and Development**\\n\\nYour 350+ word history here...\\n\\n[continue for all 8 sections with detailed content]",
  "sources": ["Wikipedia: Source1", "Web: Source2", "Wikipedia: Source3"],
  "tools_used": ["Wikipedia", "Web Search"]
}}
""",
        ),
        (
            "human",
            """
Research Topic: {query}

Create a comprehensive 2000+ word research summary with the 8 sections listed above.

Wikipedia Content: {wiki_context}
Web Search Content: {search_context}

Return ONLY the JSON object with topic, summary, sources, and tools_used fields. Make the summary very detailed with all 8 sections.
""",
        ),
    ]
)

chain = prompt | llm

# ------------------------
# Input Card
# ------------------------
with st.container():
    st.markdown("### Research Topic")

    query = st.text_input(
        "",
        placeholder="Arrow of Time, Quantum Paradox, General Relativity..."
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        save_result = st.checkbox(" Save to file")

    run = st.button(" Start Research", use_container_width=True)

# ------------------------
# Research Execution
# ------------------------
if run and query:
    with st.spinner("Exploring the universe of knowledge… 🌌"):
        wiki_context = wiki_tool.run(query)
        search_context = search_tool.run(query)

        raw = chain.invoke(
            {
                "query": query,
                "wiki_context": wiki_context,
                "search_context": search_context,
            }
        )

    try:
        # Clean the raw response content
        raw_content = raw.content.strip()
        
        # Remove any markdown formatting if present
        if raw_content.startswith('```json'):
            raw_content = raw_content.replace('```json', '').replace('```', '').strip()
        
        # Fix common JSON issues
        import json
        
        # Try direct parsing first
        try:
            # Parse as JSON directly
            json_data = json.loads(raw_content)
            
            # Create ResearchResponse object manually
            result = ResearchResponse(
                topic=json_data.get("topic", "Research Topic"),
                summary=json_data.get("summary", ""),
                sources=json_data.get("sources", []),
                tools_used=json_data.get("tools_used", [])
            )
            
        except json.JSONDecodeError:
            # If direct parsing fails, try to fix common issues
            # Fix newlines in JSON strings
            fixed_content = raw_content.replace('\n', '\\n').replace('\r', '\\r')
            # Fix any unescaped quotes in the summary
            import re
            # This is a more complex fix - let's try the parser again
            result = parser.parse(raw_content)

        st.success("Research completed successfully!")

        st.divider()

        # ------------------------
        # Results Card
        # ------------------------
        with st.container():
            st.markdown("## 📌 Topic")
            st.markdown(f"**{result.topic}**")
            
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("##  Detailed Summary")
            # Display summary with proper formatting and enhanced subheadings
            summary_text = result.summary
            # Handle escaped newlines
            if '\\n\\n' in summary_text:
                summary_text = summary_text.replace('\\n\\n', '\n\n').replace('\\n', '\n')
            
            # Enhance subheadings - make them larger and add spacing
            import re
            
            # Replace **Section Name** with larger headings and add spacing
            summary_text = re.sub(
                r'\*\*(.*?)\*\*', 
                r'<br><h3 style="color: #2E86AB; font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1rem; font-weight: 600;">\1</h3>', 
                summary_text
            )
            
            # Display with enhanced formatting
            st.markdown(summary_text, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)

            st.markdown("## 📚 Sources")
            for src in result.sources:
                st.markdown(f"- {src}")
            
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("## 🛠 Tools Used")
            cols = st.columns(2)
            for i, tool in enumerate(result.tools_used):
                cols[i % 2].markdown(f"- {tool}")

        if save_result:
            save_tool.invoke(json.dumps(result.model_dump(), indent=4))
            st.toast("Saved to research_output.txt 📄")

    except Exception as e:
        st.error("❌ Failed to parse model output")
        st.write("**Error details:**", str(e))
        
        # The content is actually good, let's extract and display it manually
        try:
            import json
            raw_content = raw.content.strip()
            
            # Try to parse the JSON manually
            json_data = json.loads(raw_content)
            
            # Display the content even if Pydantic parsing failed
            st.success("✅ Content extracted successfully (manual parsing)")
            st.divider()
            
            st.markdown("## 📌 Topic")
            st.markdown(f"**{json_data.get('topic', 'Research Topic')}**")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("## 🧠 Detailed Summary")
            summary = json_data.get('summary', '')
            # Handle newlines properly
            if '\\n' in summary:
                summary = summary.replace('\\n\\n', '\n\n').replace('\\n', '\n')
            
            # Enhance subheadings - make them larger and add spacing
            import re
            summary = re.sub(
                r'\*\*(.*?)\*\*', 
                r'<br><h3 style="color: #2E86AB; font-size: 1.5rem; margin-top: 2rem; margin-bottom: 1rem; font-weight: 600;">\1</h3>', 
                summary
            )
            
            st.markdown(summary, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            st.markdown("## 📚 Sources")
            for src in json_data.get('sources', []):
                st.markdown(f"- {src}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.markdown("## 🛠 Tools Used")
            tools = json_data.get('tools_used', [])
            cols = st.columns(2)
            for i, tool in enumerate(tools):
                cols[i % 2].markdown(f"- {tool}")
            
            # Save if requested
            if save_result:
                save_tool.invoke(json.dumps(json_data, indent=4))
                st.toast("Saved to research_output.txt 📄")
                
        except Exception as inner_e:
            st.write("Could not extract content:", str(inner_e))
            
            # Last resort - try to extract just the summary
            try:
                raw_content = raw.content
                if '"summary":' in raw_content:
                    import re
                    summary_match = re.search(r'"summary":\s*"([^"]*(?:\\.[^"]*)*)"', raw_content, re.DOTALL)
                    if summary_match:
                        summary_content = summary_match.group(1).replace('\\n', '\n').replace('\\"', '"')
                        st.markdown("## 📄 Extracted Summary Content")
                        st.markdown(summary_content)
                
                with st.expander("View raw output"):
                    st.code(raw_content)
                    
            except Exception as final_e:
                st.write("Final extraction failed:", str(final_e))
                with st.expander("View raw output"):
                    st.code(raw.content)
