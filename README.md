# Snowflake Generative AI Tools

<img src="Snowflake.svg" width="100">

A Streamlit application that demonstrates various Generative AI capabilities powered by Snowflake Cortex and a variety of foundation models.

## Overview

This application provides a user-friendly interface to interact with Snowflake's Generative AI capabilities through Streamlit. It leverages Snowflake Cortex and various LLM models to demonstrate different AI functionalities such as transcription, translation, sentiment analysis, data summarization, text classification, and more.

## Features

- **Transcription**: Transcribe audio files using Snowflake Cortex
- **Translation**: Translate text between 11 different languages using Snowflake Cortex
- **Sentiment Analysis**: Analyze the sentiment of call transcripts
- **Data Summarization**: Generate concise summaries of large text datasets
- **Next Best Action**: Use foundation models to identify customer next actions
- **Text Classification**: Categorize text into predefined categories
- **Email Generation**: Create customer emails based on call transcripts
- **Question Answering**: Ask questions to foundation models
- **Multi-Modal Image Analysis**: Analyze and categorize images using multi-modal models

## Supported Models

The application supports a wide range of foundation models including:

- Claude 4 Sonnet
- Claude 3.7 Sonnet
- Snowflake Arctic
- Llama 4 (Maverick and Scout)
- Deepseek R1
- Mistral Large/Large2
- Reka models
- Mixtral
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
   This is designed to be run inside of Snowflake: "Streamlit in Snowflake"
   ```

2. Use the sidebar to navigate between different Generative AI tools

3. For Multi-Modal Audio Transcription:
   - Upload an audio file
   - Play the audio file
   - Get detailed transcription in JSON format

4. For Multi-Modal Image Analysis:
   - Upload an image file
   - Select a multi-modal model (Claude 3.5 Sonnet or Pixtral Large)
   - Get detailed information about the image in JSON format

## File Handling

The application creates a Snowflake stage if it doesn't exist and allows you to upload files to it. Supported file extensions for preview include:
- .csv
- .txt
- .tsv
- .png
- .jpg
- .jpeg
- .gif
- .webp
- .img
- .mp3

## Notes

- The app integrates with Snowflake's session using `get_active_session()`
- Custom CSS is applied to style the sidebar
- Make sure to have the appropriate permissions in your Snowflake account to use all features

## Example Code

Here's an example of how the application calls Snowflake Cortex for sentiment analysis:

```python
sent_cortex_response = session.sql(
    f"select snowflake.cortex.sentiment('{sent_entered_transcript}') as sentiment"
).to_pandas()
```

## Customization

You can customize the model prompts, the list of available models, and other parameters according to your specific use case.


