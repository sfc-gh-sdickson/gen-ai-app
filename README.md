# Snowflake Generative AI Tools

![Snowflake Logo](Snowflake.svg,100)

A Streamlit application that demonstrates various Generative AI capabilities powered by Snowflake Cortex and a variety of foundation models.

## Overview

This application provides a user-friendly interface to interact with Snowflake's Generative AI capabilities through Streamlit. It leverages Snowflake Cortex and various LLM models to demonstrate different AI functionalities such as translation, sentiment analysis, data summarization, text classification, and more.

## Features

- **Translation**: Translate text between 11 different languages using Snowflake Cortex
- **Sentiment Analysis**: Analyze the sentiment of call transcripts
- **Data Summarization**: Generate concise summaries of large text datasets
- **Next Best Action**: Use foundation models to identify customer next actions
- **Text Classification**: Categorize text into predefined categories
- **Email Generation**: Create customer emails based on call transcripts
- **Question Answering**: Ask questions to foundation models
- **Code Conversion**: Convert code for use in Snowflake SQL
- **Multi-Modal Image Analysis**: Analyze and categorize images using multi-modal models

## Supported Models

The application supports a wide range of foundation models including:

- Claude 3.5 Sonnet - Primary Model for this Project
- Snowflake Arctic
- Llama 4 (Maverick and Scout)
- Deepseek R1
- Mistral Large/Large2
- Reka models
- Mixtral
- Llama 3/3.1/3.2 variants
- And more...

## Prerequisites

- Snowflake account with Cortex and Snowpark capabilities enabled
- Appropriate permissions to create stages and access Snowflake Cortex
- Streamlit installed in your environment

## Setup

1. Make sure you have an active Snowflake session
2. The app uses Snowflake's Snowpark for Python integration
3. SVG files (`Snowflake.svg` and `Bear-Skater_ICE.svg`) need to be in the same directory as the app

## Usage

1. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

2. Use the sidebar to navigate between different Generative AI tools

3. For Multi-Modal Image Analysis:
   - Upload an image file
   - Select a multi-modal model (Claude 3.5 Sonnet or Pixtral Large)
   - Get detailed information about the image in JSON format

## File Handling

The application creates a Snowflake stage if it doesn't exist and allows you to upload files to it. Supported file extensions for preview include:
- .csv
- .txt
- .tsv

## Notes

- The app integrates with Snowflake's session using `get_active_session()`
- Custom CSS is applied to style the sidebar
- Make sure to have the appropriate permissions in your Snowflake account to use all features

## Example Code

Here's an example of how the application calls Snowflake Cortex for sentiment analysis:

```python
cortex_response = session.sql(
    f"select snowflake.cortex.sentiment('{entered_transcript}') as sentiment"
).to_pandas()
```

## Customization

You can customize the model prompts, the list of available models, and other parameters according to your specific use case.

## License

[Insert your license information here]

## Contributing

[Insert contribution guidelines here]
