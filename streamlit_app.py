# Import required libraries
import streamlit as st
import altair as alt
import pandas as pd
import json
import os
import io
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark import DataFrame
from snowflake.snowpark.context import get_active_session

# Constants
images_stage = "images_stage"

# Configure Streamlit page layout
st.set_page_config(layout="wide")

# Custom CSS styling for sidebar
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

# Initialize Snowflake session
session = get_active_session()

def toolsapp():
    """Display the welcome page with logos and header"""
    with st.container():
        def read_svg(path):
            """Helper function to read SVG files"""
            with open(path, 'r') as f:
                svg_string = f.read()
            return svg_string

        # Load and display SVG images
#        svg_content = read_svg("Snowflake.svg")
#        svg_content2 = read_svg("Bear-Skater_ICE.svg")
#        st.image(svg_content, width=100)
        st.header("Welcome to Your New Generative AI Tools App!")
#        st.image(svg_content2, width=500)

def translate():
    with st.container():
        st.header("Translate With Snowflake Cortex")
        supported_languages = {
            "German": "de",
            "French": "fr",
            "Korean": "ko",
            "Portuguese": "pt",
            "English": "en",
            "Italian": "it",
            "Russian": "ru",
            "Swedish": "sv",
            "Spanish": "es",
            "Japanese": "ja",
            "Polish": "pl"
        }
        
        col1, col2 = st.columns(2)
        with col1:
            from_language = st.selectbox(
                "From", dict(sorted(supported_languages.items()))
            )
        with col2:
            to_language = st.selectbox("To", dict(sorted(supported_languages.items())))
        entered_text = st.text_area(
            "Enter text",
            label_visibility="hidden",
            height=300,
            placeholder="For example: call transcript",
        )
        if entered_text:
            entered_text = entered_text.replace("'", "\\'")
            cortex_response = (
                session.sql(
                    f"select snowflake.cortex.translate('{entered_text}','{supported_languages[from_language]}','{supported_languages[to_language]}') as response"
                )
                .to_pandas()
                .iloc[0]["RESPONSE"]
            )
            st.write(cortex_response)

def sentiment():
    with st.container():
        st.header("Sentiment Analysis With Snowflake Cortex")
        # Sample transcript
        # Customer: Hello! Agent: Hello! I hope you're having a great day. To best assist you, can you please share your first and last name and the company you're calling from? Customer: Sure, I'm Michael Green from SnowSolutions. Agent: Thanks, Michael! What can I help you with today? Customer: We recently ordered several DryProof670 jackets for our store, but when we opened the package, we noticed that half of the jackets have broken zippers. We need to replace them quickly to ensure we have sufficient stock for our customers. Our order number is 60877. Agent: I apologize for the inconvenience, Michael. Let me look into your order. It might take me a moment. Customer: Thank you. Agent: Michael, I've confirmed your order and the damage. Fortunately, we currently have enough stock to replace the damaged jackets. We'll send out the replacement jackets immediately, and they should arrive within 3-5 business days. Customer: That's great to hear! How should we handle returning the damaged jackets? Agent: We will provide you with a return shipping label so that you can send the damaged jackets back to us at no cost to you. Please place the jackets in the original packaging or a similar box. Customer: Sounds good! Thanks for your help. Agent: You're welcome, Michael! We apologize for the inconvenience, and thank you for your patience. Please don't hesitate to contact us if you have any further questions or concerns. Have a great day! Customer: Thank you! You too.
        entered_transcript = st.text_area(
            "Enter call transcript",
            label_visibility="hidden",
            height=400,
            placeholder="Enter call transcript",
        )
        entered_transcript = entered_transcript.replace("'", "\\'")
        if entered_transcript:
            cortex_response = session.sql(
                f"select snowflake.cortex.sentiment('{entered_transcript}') as sentiment"
            ).to_pandas()
            st.caption(
                "Score is between -1 and 1; -1 = Most negative, 1 = Positive, 0 = Neutral"
            )
            # st.write(cortex_response)
            st.dataframe(cortex_response, hide_index=True, width=100)

def supersum():
    with st.container():
        st.header("Summarize Data With Snowflake Cortex")
        entered_text = st.text_area(
            "Enter data to summarize",
            label_visibility="hidden",
            height=400,
            placeholder="Enter data to summarize",
        )
        entered_text = entered_text.replace("'", "\\'")
        if entered_text:
            cortex_response = session.sql(
                f"select snowflake.cortex.summarize('{entered_text}') as RESPONSE").to_pandas().iloc[0]["RESPONSE"];
        
            st.caption("Summarized data:")
            # df_string = cortex_response.to_string(index=False)
            # st.write(df_string)
            #st.dataframe(cortex_response, hide_index=True, width=1100)
            st.write(cortex_response)

def nextba():
    with st.container():
        st.header("Use a Snowflake Foundational LLM to Identify Customer Next Best Action")
        model_list = [
            "claude-3-5-sonnet",
            "deepseek-r1",
            "snowflake-arctic",
            "mistral-large",
            "mistral-large2",
            "reka-flash",
            "reka-core",
            "jamba-instruct",
            "jamba-1.5-mini",
            "jamba-1.5-large",
            "mixtral-8x7b",
            "llama2-70b-chat",
            "llama3-8b",
            "llama3-70b",
            "llama3.1-8b",
            "llama3.1-70b",
            "llama3.1-405b",
            "llama3.2-1b",
            "llama3.2-3b",
            "mistral-7b",
            "gemma-7b",
        ]
        selected_model = st.selectbox("Which Foundational Model:", model_list)
        entered_code = st.text_area(
            "Paste the Data for Your Question",
            label_visibility="hidden",
            height=300,
            placeholder="Paste Data",
        )
        entered_code = entered_code.replace("'", "\\'")
        default_model_instruct = """Based on these data, please provide the next best action"""
        model_instruct = st.text_area(
            "Please provide Model Instructions",
            default_model_instruct,
            label_visibility="hidden",
            placeholder="Enter Prompt",
        )

        if st.button("Next Best Action!"):
            cortex_response = session.sql(
                    f"select snowflake.cortex.complete('{selected_model}',concat('[INST]','{model_instruct}','{entered_code}','[/INST]')) as RESPONSE").to_pandas().iloc[0]["RESPONSE"];
            st.caption("Answer:")
            #st.dataframe(cortex_response, hide_index=True, width=1100)
            st.write(cortex_response)

def classify():
    with st.container():
        st.header("Classify Data With Snowflake Cortex")
        entered_text = st.text_area(
            "Enter data to Classify",
            label_visibility="hidden",
            height=400,
            placeholder="Enter data to classify",
        )
        entered_text = entered_text.replace("'", "\\'")

        if entered_text:
            cortex_response = session.sql(
                f"select snowflake.cortex.classify_text('{entered_text}',['Refund','Exchange','No Category']) as Answer"
            ).to_pandas().iloc[0]["ANSWER"];
            st.caption("Classified data:")
            st.write(cortex_response)
            # st.dataframe(cortex_response, hide_index=True, width=200)

def emailcomplete():
    with st.container():
        st.header("Generate a Customer E-Mail With Snowflake Cortex Complete")
        model_list = [
            "claude-3-5-sonnet",
            "snowflake-arctic",
            'llama4-maverick',
            'llama4-scout',
            "deepseek-r1",
            "mistral-large",
            "mistral-large2",
            "reka-flash",
            "reka-core",
            "jamba-instruct",
            "jamba-1.5-mini",
            "jamba-1.5-large",
            "mixtral-8x7b",
            "llama2-70b-chat",
            "llama3-8b",
            "llama3-70b",
            "llama3.1-8b",
            "llama3.1-70b",
            "llama3.1-405b",
            "llama3.2-1b",
            "llama3.2-3b",
            "mistral-7b",
            "gemma-7b",
        ]
        selected_model = st.selectbox("Which Foundational Model:", model_list)
        entered_code = st.text_area(
            "Paste the Call Transcript to use for E-Mail Generation:",
            label_visibility="hidden",
            height=300,
            placeholder="Paste Call Transcript",
        )
        entered_code = entered_code.replace("'", "\\'")
        default_model_instruct = """Please create an email for me that describes the issue in detail and provides a solution.     Make the e-mail from me, the Director of Customer Relations at Ski Gear Co, and also give the customer a 10% discount with code: CS10OFF"""
        model_instruct = st.text_area(
            "Please Provide E-Mail Generation Model Instructions: ",
            default_model_instruct,
            label_visibility="hidden",
            placeholder="Enter Prompt",
        )

        if st.button("Generate E-Mail"):
            cortex_response = session.sql(
                f"select snowflake.cortex.complete('{selected_model}',concat('[INST]','{model_instruct}','{entered_code}','[/INST]')) as RESPONSE").to_pandas().iloc[0]["RESPONSE"];
            st.caption("Customer E-Mail:")
            #st.dataframe(cortex_response, hide_index=True, width=1100)
            st.write(cortex_response)

def askaquestion():
    with st.container():
        st.header("Use a Snowflake Foundational LLM to Ask a Question")
        model_list = [
            "claude-3-5-sonnet",
            "snowflake-arctic",
            'llama4-maverick',
            'llama4-scout',
            "deepseek-r1",
            "mistral-large",
            "mistral-large2",
            "reka-flash",
            "reka-core",
            "jamba-instruct",
            "jamba-1.5-mini",
            "jamba-1.5-large",
            "mixtral-8x7b",
            "mistral-7b",
            "gemma-7b",
        ]
        selected_model = st.selectbox("Which Foundational Model:", model_list)
        entered_code = st.text_area(
            "Paste the Data for Your Question",
            label_visibility="hidden",
            height=300,
            placeholder="Paste Data",
        )
        entered_code = entered_code.replace("'", "\\'")
        model_instruct = st.text_area(
            "Please provide Model Instructions",
            label_visibility="hidden",
            placeholder="Enter Prompt",
        )

        if st.button("Ask My Question!"):
            cortex_response = session.sql(
                    f"select snowflake.cortex.complete('{selected_model}',concat('[INST]','{model_instruct}','{entered_code}','[/INST]')) as RESPONSE").to_pandas().iloc[0]["RESPONSE"];
            st.caption("Answer:")
            #st.dataframe(cortex_response, hide_index=True, width=1100)
            st.write(cortex_response)

def codeconvert():
    with st.container():
        st.header("Use a Snowflake Foundational LLM to Test Code Conversion")
        default_model_instruct = """Please convert this code for use in Snowflake SQL and validate that it will run in Snowflake:"""
        default_code_convert = """USE AdventureWorks2022;
                    GO

                    IF OBJECT_ID('dbo.NewProducts', 'U') IS NOT NULL
                    DROP TABLE dbo.NewProducts;
                    GO

                    ALTER DATABASE AdventureWorks2022 SET RECOVERY BULK_LOGGED;
                    GO

                    SELECT *
                    INTO dbo.NewProducts
                    FROM Production.Product
                    WHERE ListPrice > $25
                              AND ListPrice < $100;
                    GO

                    ALTER DATABASE AdventureWorks2022 SET RECOVERY FULL;
                    GO
                    """
        model_list = [
            "claude-3-5-sonnet",
            "snowflake-arctic",
            'llama4-maverick',
            'llama4-scout',
            "deepseek-r1",
            "mistral-large",
            "mistral-large2",
            "reka-flash",
            "reka-core",
            "jamba-instruct",
            "jamba-1.5-mini",
            "jamba-1.5-large",
            "mixtral-8x7b",
            "mistral-7b",
            "gemma-7b",
        ]
        selected_model = st.selectbox("Which Foundational Model:", model_list)
        entered_code = st.text_area(
            "Paste the Code You Would Like to Convert",
            default_code_convert,
            label_visibility="hidden",
            height=300,
            placeholder="Paste Code for Conversion",
        )
        entered_code = entered_code.replace("'", "\\'")
        model_instruct = st.text_area(
            "Please provide Model Instructions: ",
            default_model_instruct,
            label_visibility="hidden",
            placeholder="Enter Prompt",
        )

        if st.button("Run Conversion"):
            cortex_response = session.sql(
                f"select snowflake.cortex.complete('{selected_model}',concat('[INST]','{model_instruct}','{entered_code}','[/INST]')) as RESPONSE").to_pandas().iloc[0]["RESPONSE"];
            st.caption("Converted Code:")
            st.write(cortex_response)

# -------------------------------------
# Constants and settings
# -------------------------------------
# File extensions that can be previewed
PREVIEWABLE_EXTENSIONS = ['.csv', '.txt', '.tsv']

# -------------------------------------
# Stage existence check and creation
# -------------------------------------
def ensure_stage_exists(stage_name_no_at: str):
    """
    Creates a stage if it doesn't exist. Does nothing if it already exists.
    """
    try:
        # Check if stage exists
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
            st.stop()

# -------------------------------------
# Main Streamlit app
# -------------------------------------
def mmimage():
    st.subheader("File Upload")
    st.write("Upload files to Snowflake stage.")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        try:
            # Create file stream using BytesIO and upload
            file_stream = io.BytesIO(uploaded_file.getvalue())
            session.file.put_stream(
                file_stream,
                f"{images_stage}/{uploaded_file.name}",
                auto_compress=False,
                overwrite=True
            )
            
            st.success(f"File '{uploaded_file.name}' has been uploaded successfully!")

            # Define image in a stage and read the file
            image_file=session.file.get_stream(f'@{images_stage}/{uploaded_file.name}' , decompress=False).read() 

            # Display the image
            st.image(image_file, width=300)

            llm_selection = st.selectbox(
                "Select an Large Language Model:",
                options=["claude-3-5-sonnet", "pixtral-large"]
            )
            
            user_prompt = st.text_input(
                "Enter a prompt for the AI model:",
                value="Please provide a concise description of this image."
            )

            if st.button("Run AI Model"):
                if user_prompt:
                    image_text = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.COMPLETE('{llm_selection}',
                            'Please provide a concise description of this image.',
                            TO_FILE('@{images_stage}', '{uploaded_file.name}')
                        );""").collect()
            
                    st.write(image_text[0][0])
        
        except Exception as e:
            st.error(f"Error occurred while uploading file: {str(e)}")

# Dictionary mapping page names to their corresponding functions
page_names_to_funcs = {
    "Tools App": toolsapp,
    "Translation": translate,
    "Sentiment Analysis": sentiment,
    "Summarize": supersum,
    "Next Best Action": nextba,
    "Classify": classify,
    "Generate E-Mail": emailcomplete,
    "Ask a Question": askaquestion,
    "Code Conversion": codeconvert,
    "Multi-Modal Image Analysis": mmimage
}

# Sidebar navigation
selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
