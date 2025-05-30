# Import required libraries
import streamlit as st  # Web app framework
import altair as alt    # Data visualization library
import pandas as pd     # Data manipulation and analysis
import json            # JSON data handling
import os              # Operating system interface
import io              # Input/output operations
import time            # Time-related functions

# Snowflake-specific imports
from snowflake.snowpark.context import get_active_session  # Get active Snowflake session
from snowflake.snowpark.functions import col               # Column functions for Snowpark
from snowflake.snowpark import DataFrame                   # Snowpark DataFrame class
from datetime import datetime                              # Date and time handling
from streamlit_extras.stylable_container import stylable_container  # Custom styled containers

# Initialize Snowflake session - establishes connection to Snowflake
session = get_active_session()

# Configure Streamlit page layout to use full width
st.set_page_config(layout="wide")

# Custom CSS styling for sidebar - sets background color and text color
st.markdown(
    """
          <style type="text/css">
          [data-testid=stSidebar] {
                    background-color: rgb(129, 164, 225);
                    color: #FFFFFF;
          }
          </style>
""",
    unsafe_allow_html=True,
)

# CSS styling for card components - defines border, shadow, and padding
card_style = """
    {
        border: 1px groove #52546a;
        border-radius: 10px;
        padding-left: 25px;
        padding-top: 10px;
        padding-bottom: 10px;
        box-shadow: -6px 8px 20px 1px #00000052;
    }
"""

def toolsapp():
    """Display the welcome page with logos and header information"""
    with st.container():
        # Load SVG images for branding
        svg_content = read_svg("Snowflake.svg")      # Snowflake logo
        svg_content2 = read_svg("Bear-Skater_ICE.svg")  # Bear mascot image

        # Create two columns for layout - logo and main content
        cl1, cl2 = st.columns([1,4])

        with cl1:
            # Display Snowflake logo in left column
            st.image(svg_content, width=100)

        with cl2:
            # Display main welcome content in right column
            with stylable_container("Card1", css_styles=card_style):
                st.write(" ")  # Add spacing

            # Main title and subtitle with help text
            st.metric("Unlock Insights from Unstructured Data with Snowflake Cortex AI", 
                     "Snowflake Summit HOL: AI209", 
                     help="Tools for Every Day AI")
            st.subheader("Welcome to Your New Generative AI Tools App!")

            # Add styled spacing
            with stylable_container("Card1", css_styles=card_style):
                st.write(" ")

            # Display bear mascot image
            st.image(svg_content2, width=500)

def translate():
    """Translation functionality using Snowflake Cortex AI"""
    with st.container():
        # Display header with logo
        svg_content = read_svg("Snowflake.svg")
        st.image(svg_content, width=100)
        st.header("Translate With Snowflake Cortex")

        # Dictionary of supported languages with their language codes
        supported_languages = {
            "German": "de", "French": "fr", "Hindi": "hi", "Korean": "ko",
            "Portuguese": "pt", "English": "en", "Italian": "it", "Russian": "ru",
            "Swedish": "sv", "Spanish": "es", "Japanese": "ja", "Arabic": "ar",
            "Polish": "pl"
        }

        # Create two columns for language selection
        col1, col2 = st.columns(2)
        with col1:
            # Source language dropdown
            from_language = st.selectbox(
                "From", dict(sorted(supported_languages.items()))
            )
        with col2:
            # Target language dropdown
            to_language = st.selectbox("To", dict(sorted(supported_languages.items())))

        # Text area for input text to translate
        xlate_entered_text = st.text_area(
            "Enter text",
            label_visibility="hidden",
            height=300,
            placeholder="For example: call transcript",
        )

        # Process translation if text is entered
        if xlate_entered_text:
            # Escape single quotes to prevent SQL injection
            xlate_entered_text = xlate_entered_text.replace("'", "\\'")

            # Call Snowflake Cortex translate function via SQL
            xlate_cortex_response = (
                session.sql(f"select snowflake.cortex.translate('{xlate_entered_text}','{supported_languages[from_language]}','{supported_languages[to_language]}') as response").to_pandas().iloc[0]["RESPONSE"])
            # Display translated text
            st.write(xlate_cortex_response)

def sentiment():
    """Sentiment analysis functionality using Snowflake Cortex AI"""
    with st.container():
        st.header("Sentiment Analysis With Snowflake Cortex")

        # Text area for entering transcript or text to analyze
        sent_entered_transcript = st.text_area(
            "Enter call transcript",
            label_visibility="hidden",
            height=400,
            placeholder="Enter call transcript",
        )

        # Escape single quotes for SQL safety
        sent_entered_transcript = sent_entered_transcript.replace("'", "\\'")

        # Process sentiment analysis if text is entered
        if sent_entered_transcript:
            # Call Snowflake Cortex sentiment analysis function
            sent_cortex_response = session.sql(f"select snowflake.cortex.sentiment('{sent_entered_transcript}') as sentiment").to_pandas();

            st.caption(
                "Score is between -1 and 1; -1 = Most negative, 1 = Positive, 0 = Neutral"
            )
            # Display sentiment results in a dataframe
            st.dataframe(sent_cortex_response, hide_index=True, width=100)

def supersum():
    """Text summarization functionality using Snowflake Cortex AI"""
    with st.container():
        st.header("Summarize Data With Snowflake Cortex")

        # Text area for entering data to summarize
        ssum_entered_text = st.text_area(
            "Enter data to summarize",
            label_visibility="hidden",
            height=400,
            placeholder="Enter data to summarize",
        )

        # Escape single quotes for SQL safety
        ssum_entered_text = ssum_entered_text.replace("'", "\\'")

        # Process summarization if text is entered
        if ssum_entered_text:
            # Call Snowflake Cortex summarize function
            ssum_cortex_response = session.sql(
                f"select snowflake.cortex.summarize('{ssum_entered_text}') as RESPONSE"
            ).to_pandas().iloc[0]["RESPONSE"]

            # Display summarized results
            st.caption("Summarized data:")
            st.write(ssum_cortex_response)

def nextba():
    """Next Best Action recommendation using Snowflake foundational LLMs"""
    with st.container():
        st.header("Use a Snowflake Foundational LLM to Identify Customer Next Best Action")

        # List of available foundational models
        model_list = [
            "claude-4-sonnet", "claude-3-7-sonnet", 'llama4-maverick', 'llama4-scout',
            "deepseek-r1", "snowflake-arctic", "mistral-large2", "reka-flash",
            "reka-core", "llama3.1-405b", "llama3.2-1b", "llama3.2-3b", "mistral-7b"
        ]

        # Model selection dropdown
        next_selected_model = st.selectbox("Which Foundational Model:", model_list)

        # Text area for input data
        next_entered_code = st.text_area(
            "Paste the Data for Your Question",
            label_visibility="hidden",
            height=300,
            placeholder="Paste Data",
        )

        # Escape single quotes for SQL safety
        next_entered_code = next_entered_code.replace("'", "\\'")

        # Default instruction prompt for the model
        next_default_model_instruct = """Based on these data, please provide the next best action"""

        # Text area for custom model instructions
        next_model_instruct = st.text_area(
            "Please provide Model Instructions",
            next_default_model_instruct,
            label_visibility="hidden",
            placeholder="Enter Prompt",
        )

        # Button to trigger next best action analysis
        if st.button("Next Best Action!"):
            # Call Snowflake Cortex complete function with selected model
            next_cortex_response = session.sql(
                f"select snowflake.cortex.complete('{next_selected_model}',concat('[INST]','{next_model_instruct}','{next_entered_code}','[/INST]')) as RESPONSE"
            ).to_pandas().iloc[0]["RESPONSE"]

            # Display the recommendation
            st.caption("Answer:")
            st.write(next_cortex_response)

def classify():
    """Text classification functionality using Snowflake Cortex AI"""
    with st.container():
        st.header("Classify Data With Snowflake Cortex")

        # Text area for data to classify
        class_entered_text = st.text_area(
            "Enter data to Classify",
            label_visibility="hidden",
            height=400,
            placeholder="Enter data to classify",
        )

        # Escape single quotes for SQL safety
        class_entered_text = class_entered_text.replace("'", "\\'")

        # Process classification if text is entered
        if class_entered_text:
            # Call Snowflake Cortex classify_text function with predefined categories
            class_cortex_response = session.sql(
                f"select snowflake.cortex.ai_classify('{class_entered_text}',['Complete Refund','Exchange Tickets','Refund Fees', 'Discount Sale','Send a Nice Thank You E-mail']) as Answer"
            ).to_pandas().iloc[0]["ANSWER"]

            # Display classification result
            st.caption("Classified data:")
            st.write(class_cortex_response)

def emailcomplete():
    """Email generation functionality using Snowflake foundational LLMs"""
    with st.container():
        st.header("Generate a Customer E-Mail With Snowflake Cortex Complete")

        # List of available models for email generation
        model_list = [
            "claude-4-sonnet", "claude-3-7-sonnet", "snowflake-arctic",
            'llama4-maverick', 'llama4-scout', "deepseek-r1", "mistral-large",
            "reka-flash", "reka-core", "llama3.1-405b"
        ]

        # Model selection dropdown
        email_selected_model = st.selectbox("Which Foundational Model:", model_list)

        # Text area for call transcript input
        email_entered_code = st.text_area(
            "Paste the Call Transcript to use for E-Mail Generation:",
            label_visibility="hidden",
            height=300,
            placeholder="Paste Call Transcript",
        )

        # Escape single quotes for SQL safety
        email_entered_code = email_entered_code.replace("'", "\\'")

        # Default email generation instructions
        email_default_model_instruct = """Please create an email for me that describes the issue in detail and provides a solution. Make the e-mail from me, the Director of Customer Relations at The Big Ticket Co, and also give the customer a 10% discount with code: CS10OFF of a future order"""

        # Text area for custom email instructions
        email_model_instruct = st.text_area(
            "Please Provide E-Mail Generation Model Instructions: ",
            email_default_model_instruct,
            label_visibility="hidden",
            placeholder="Enter Prompt",
        )

        # Button to trigger email generation
        if st.button("Generate E-Mail"):
            # Call Snowflake Cortex complete function for email generation
            email_cortex_response = session.sql(
                f"select snowflake.cortex.complete('{email_selected_model}',concat('[INST]','{email_model_instruct}','{email_entered_code}','[/INST]')) as RESPONSE"
            ).to_pandas().iloc[0]["RESPONSE"]

            # Display generated email
            st.caption("Customer E-Mail:")
            st.write(email_cortex_response)

def askaquestion():
    """General question-answering functionality using Snowflake foundational LLMs"""
    with st.container():
        st.header("Use a Snowflake Foundational LLM to Ask a Question")

        # List of available models for Q&A
        model_list = [
            "claude-4-sonnet", "claude-3-7-sonnet", "snowflake-arctic",
            'llama4-maverick', 'llama4-scout', "deepseek-r1", "mistral-large2",
            "reka-flash", "reka-core", "mixtral-8x7b"
        ]

        # Model selection dropdown
        askq_selected_model = st.selectbox("Which Foundational Model:", model_list)

        # Text area for context data
        askq_entered_code = st.text_area(
            "Paste the Data for Your Question",
            label_visibility="hidden",
            height=300,
            placeholder="Paste Data",
        )

        # Escape single quotes for SQL safety
        askq_entered_code = askq_entered_code.replace("'", "\\'")

        # Text area for the actual question/prompt
        askq_model_instruct = st.text_area(
            "Please provide Model Instructions",
            label_visibility="hidden",
            placeholder="Enter Prompt",
        )

        # Button to submit question
        if st.button("Ask My Question!"):
            # Call Snowflake Cortex complete function with question and data
            askq_cortex_response = session.sql(
                f"select snowflake.cortex.complete('{askq_selected_model}',concat('[INST]','{askq_model_instruct}','{askq_entered_code}','[/INST]')) as RESPONSE"
            ).to_pandas().iloc[0]["RESPONSE"]

            # Display the answer
            st.caption("Answer:")
            st.write(askq_cortex_response)

#-------------------------------------
# Constants and settings for file handling
# -------------------------------------
# File extensions that can be previewed in the application
PREVIEWABLE_EXTENSIONS = ['.txt', '.tsv', '.csv', '.jpg', '.img', '.webp', '.jpeg', '.mp3', '.mpg4']

# -------------------------------------
# Stage existence check and creation
# -------------------------------------
def ensure_stage_exists(stage_name_no_at: str):
    """
    Creates a Snowflake stage if it doesn't exist. Does nothing if it already exists.

    Args:
        stage_name_no_at (str): Stage name without the @ prefix
    """
    try:
        # Check if stage exists by attempting to describe it
        session.sql(f"DESC STAGE {stage_name_no_at}").collect()
    except:
        # Create stage if it doesn't exist
        try:
            session.sql(f"""
                CREATE STAGE {stage_name_no_at}
                ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
            """).collect()
            st.sidebar.success(f"Stage @{stage_name_no_at} has been created.")
        except Exception as e:
            st.sidebar.error(f"Failed to create stage: {str(e)}")
            st.stop()  # Stop execution if stage creation fails

def mmimage():
    """Multi-modal image analysis functionality using Snowflake Cortex AI"""
    st.title("Multi-Modal Image Categorizer")

    # -------------------------
    # Stage settings configuration
    # -------------------------
    st.header("Stage Settings")
    # Input field for stage name
    stage_name_no_at = st.text_input(
        "Enter stage name (e.g., GENAI_STAGE)",
        "GENAI_STAGE"
    )
    stage_name = f"@{stage_name_no_at}"  # Add @ prefix for Snowflake stage reference

    # Create stage if it doesn't exist
    ensure_stage_exists(stage_name_no_at)

    # -------------------------
    # File upload section
    # -------------------------
    st.header("File Upload")
    st.write("Upload files to Snowflake stage.")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        # List of multi-modal models that can process images
        model_list = [
            "pixtral-large",
            "claude-3-7-sonnet",
            "claude-4-sonnet"
        ]

        # Get file extension for processing logic
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        try:
            # Create file stream using BytesIO and upload to Snowflake stage
            file_stream = io.BytesIO(uploaded_file.getvalue())
            session.file.put_stream(
                file_stream,
                f"{stage_name}/{uploaded_file.name}",
                auto_compress=False,
                overwrite=True
            )
            st.success(f"File '{uploaded_file.name}' has been uploaded successfully!")

            # Model selection for image analysis
            image_selected_model = st.selectbox("Which Multi-Modal Model:", model_list)

            # Default prompt for image analysis
            image_default_model_instruct = """Please provide the type of animal, breed, and environment in JSON format:
            Animal: ??,
            Breed: ??,
            Environment: ??"""

            # Text area for custom analysis instructions
            image_model_instruct = st.text_area(
                "Please Provide Model Instructions: ",
                image_default_model_instruct,
                placeholder="Enter Prompt",
                height=150
            )

            # Button to trigger image analysis
            if st.button("Image Details"):
                # Call Snowflake Cortex complete function with image file
                image_cortex_response = session.sql(
                    f"select snowflake.cortex.ai_complete('{image_selected_model}','{image_model_instruct}',TO_FILE('{stage_name}', '{uploaded_file.name}')) as RESPONSE"
                ).to_pandas().iloc[0]["RESPONSE"]

                # Display analysis results
                st.write(image_cortex_response)

            # Preview uploaded file if it's a supported format
            if file_extension in PREVIEWABLE_EXTENSIONS:
                try:
                    uploaded_file.seek(0)  # Reset file pointer to beginning

                    # Handle image and PDF files
                    if file_extension == '.webp' or '.jpg' or '.jpeg' or '.img' or '.pdf':
                        try:
                            df_preview = st.image(uploaded_file)  # Display image
                        except UnicodeDecodeError:
                            # Handle encoding issues
                            uploaded_file.seek(0)
                            df_preview = pd.read_csv(uploaded_file, encoding='shift-jis')
                    else:  # Handle text files (.txt, .tsv, etc.)
                        try:
                            df_preview = pd.read_csv(uploaded_file, sep='	')  # Tab-separated
                        except UnicodeDecodeError:
                            # Try different encoding
                            uploaded_file.seek(0)
                            df_preview = pd.read_csv(uploaded_file, sep='	', encoding='shift-jis')

                        # Display preview of tabular data
                        st.write("Preview of uploaded data:")
                        st.dataframe(df_preview.head())

                except Exception as e:
                    st.error(f"Error occurred while uploading file: {str(e)}")
        except Exception as e:
            st.error(f"Error occurred while uploading file: {str(e)}")

def mmaudio():
    """Audio transcription functionality using Snowflake AI"""
    st.title("Audio Transcription")

    # -------------------------
    # Stage settings configuration
    # -------------------------
    st.header("Stage Settings")
    # Input field for audio stage name
    stage_name_no_at = st.text_input(
        "Enter stage name (e.g., GENAI_AUDIO_STAGE)",
        "GENAI_AUDIO_STAGE"
    )
    stage_name = f"@{stage_name_no_at}"  # Add @ prefix for Snowflake stage reference

    # Create stage if it doesn't exist
    ensure_stage_exists(stage_name_no_at)

    # -------------------------
    # Audio file upload section
    # -------------------------
    st.header("File Upload")
    st.write("Upload files to Snowflake stage.")

    # File uploader widget for audio files
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        # Get file extension
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()

        try:
            # Create file stream using BytesIO and upload to Snowflake stage
            file_stream = io.BytesIO(uploaded_file.getvalue())
            session.file.put_stream(
                file_stream,
                f"{stage_name}/{uploaded_file.name}",
                auto_compress=False,
                overwrite=True
            )
            st.success(f"File '{uploaded_file.name}' has been uploaded successfully!")

            # Custom CSS styling for audio player
            style_css = """
            audio::-webkit-media-controls-panel,
            audio::-webkit-media-controls-enclosure {
                background-color: #9c9d9f;
            }"""

            # Apply custom CSS styling
            st.markdown(
                "<style>" + style_css + "</style>", unsafe_allow_html=True
            )

            # Create reference to uploaded audio file
            audio_input = stage_name + "/" + uploaded_file.name

            # Get audio file stream from Snowflake stage and display audio player
            aud = session.file.get_stream(audio_input)
            st.audio(aud, format='audio/mpeg')

            # Call Snowflake AI transcription function
            audio_cortex_response = session.sql(
                f"SELECT AI_TRANSCRIBE(TO_FILE('{stage_name}/{uploaded_file.name}')) as RESPONSE"
            ).to_pandas().iloc[0]["RESPONSE"]

            # Display transcription results
            st.write(audio_cortex_response)

        except Exception as e:
            st.error(f"Error occurred while uploading file: {str(e)}")

def read_svg(path):
    """
    Helper function to read SVG files from disk

    Args:
        path (str): Path to the SVG file

    Returns:
        str: SVG file content as string
    """
    with open(path, 'r') as f:
        svg_string = f.read()
    return svg_string

# Dictionary mapping page names to their corresponding functions
# This creates the navigation structure for the application
page_names_to_funcs = {
    "Tools App": toolsapp,                          # Welcome/home page
    "Transcribe": mmaudio,                          # Audio transcription
    "Translation": translate,                       # Text translation
    "Sentiment Analysis": sentiment,                # Sentiment analysis
    "Summarize": supersum,                         # Text summarization
    "Next Best Action": nextba,                    # Next best action recommendations
    "Classify": classify,                          # Text classification
    "Generate E-Mail": emailcomplete,              # Email generation
    "Ask a Question": askaquestion,                # General Q&A
    "Multi-Modal Image Analysis": mmimage          # Image analysis
}

# Sidebar navigation - creates dropdown menu for page selection
selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())

# Execute the selected page function
page_names_to_funcs[selected_page]()