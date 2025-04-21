summary: Unlock Insights from Unstructured Data with Snowflake Cortex AI
id: unlock_insights_from_unstructured_data_with_snowflake_cortex_ai
categories: data-engineering,ai,app-development
environments: web
status: Published
feedback link: https://github.com/Snowflake-Labs/sfguides/issues
tags: Snowflake Cortex, Generative AI, Streamlit, Snowflake, Data Applications, Multimodal AI
author: Sean Morris, Stephen Dickson

[environment_name]: ai209

# Unlock Insights from Unstructured Data with Snowflake Cortex AI
<!-- ------------------------ -->
## Overview

Duration: 5

This guide demonstrates how to create a Streamlit application running inside Snowflake that unlocks insights from unstructured data using **Snowflake Cortex AI**.  
It shows how to translate, summarize, classify text, generate emails, and even analyze images — all without deploying external infrastructure.

### Prerequisites
- Snowflake account in a [supported region for Cortex functions](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions#label-cortex-llm-availability)
- ACCOUNTADMIN role

### What You’ll Learn
- How to create a database, schema, and stage in Snowflake
- How to store unstructured data in Snowflake stages
- How to use SQL to run LLM functions (`TRANSLATE`, `SENTIMENT`, `SUMMARIZE`, `COMPLETE`)
- How to build a frontend application with Streamlit inside Snowflake

### What You'll Build
A fully functioning **Streamlit app** inside Snowflake that:
- Translates between multiple languages
- Scores sentiment of call transcripts
- Summarizes long-form text
- Classifies customer service inquiries
- Analyzes uploaded images using multimodal LLMs

<!-- ------------------------ -->
## Setup

Duration: 5

### Login to Snowsight

Log into Snowflake's web interface [Snowsight](https://docs.snowflake.com/en/user-guide/ui-snowsight.html#) using your Snowflake credentials.

### Enable Cross-Region Inference

In the Snowsight UI on the left hand sidebar, select the **Projects > Worksheets** tab.

In the top right hand corner, click the **+** button to create a new SQL worksheet.

Run the following SQL commands to [enable cortex cross-region inference](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference.html).

```sql
-- set role context
USE ROLE accountadmin;

-- enable Cortex Cross Region Inference
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';
```

### Create Snowflake Objects

In the same SQL worksheet, run the following SQL commands to create the [warehouse](https://docs.snowflake.com/en/sql-reference/sql/create-warehouse.html), [database](https://docs.snowflake.com/en/sql-reference/sql/create-database.html), [schema](https://docs.snowflake.com/en/sql-reference/sql/create-schema.html), and [stage](https://docs.snowflake.com/en/sql-reference/sql/create-stage.html)

> aside positive
> IMPORTANT:
>
> - If you use different names for objects created in this section, be sure to update scripts and code in the following sections accordingly.
>
> - For each SQL script block below, select all the statements in the block and execute them top to bottom.

```sql
-- set role context
USE ROLE sysadmin;

-- set warehouse context
CREATE WAREHOUSE IF NOT EXISTS [environment_name]_wh
    WAREHOUSE_SIZE = XSMALL
    AUTO_SUSPEND = 60
    INITIALLY_SUSPENDED = TRUE;
USE WAREHOUSE [environment_name]_wh;

-- set database and schema context
CREATE DATABASE IF NOT EXISTS [environment_name]_db;
CREATE SCHEMA IF NOT EXISTS [environment_name]_db.public;
USE SCHEMA ai209_db.public;

-- create stage to store images
CREATE STAGE IF NOT EXISTS [environment_name]_db.public.images_stage
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
```

### Download Images

Download the [images.zip](https://github.com/Snowflake-Labs/unlock-insights-from-unstructured-data-with-snowflake-cortex-ai/blob/main/images.zip) and unzip.

### Upload Images

In the Snowsight UI on the left hand sidebar, select the **Data > Databases** tab and navigate to **AI209_DB > PUBLIC > STAGE > IMAGES_STAGE**.

In the top right hand corner, click **+ Files** to upload files to your stage.

Navigate back to your SQL worksheet and run the following SQL commands to verify the images with SQL:

```sql
-- list files in stage
LIST @[environment_name]_db.public.images_stage;
```

You should see your uploaded files listed with their sizes.


TODO:

<!-- ------------------------ -->
## Create Snowflake Notebook

Duration: 15

Let's create a notebook to further explore image analysis techniques:

1. Navigate to Projects > Notebooks in Snowflake
2. Click "+ Notebook" button in the top right
3. To import the existing notebook:
   * Click the dropdown arrow next to "+ Notebook" 
   * Select "Import .ipynb" from the dropdown menu
   * Upload the [image_analysis_notebook.ipynb](https://github.com/Snowflake-Labs/sfguide-getting-started-with-image-classification-with-anthropic-snowflake-cortex/blob/main/image_analysis_notebook.ipynb) file
4. In the Create Notebook popup:
   * Select your IMAGE_ANALYSIS database and schema
   * Choose an appropriate warehouse
   * Click "Create" to finish the import

The notebook includes:
- Setup code for connecting to your Snowflake environment
- Functions for analyzing images with different AI models
- Example analysis with various prompt types
- Batch processing capabilities for multiple images
- Comparison between Claude 3.5 Sonnet and Pixtral-large models

<!-- ------------------------ -->
## Build Streamlit Application

Duration: 15

Let's create a Streamlit application for interactive image analysis:

### Setting Up the Streamlit App

To create and configure your Streamlit application in Snowflake:

1. Navigate to Streamlit in Snowflake:
   * Click on the **Streamlit** tab in the left navigation pane
   * Click on **+ Streamlit App** button in the top right

2. Configure App Settings:
   * Enter a name for your app (e.g., "Image Analyzer")
   * Select your preferred warehouse
   * Choose IMAGE_ANALYSIS as your database and schema

3. Create the app:
   * In the editor, paste the complete code provided in the [image_analysis_streamlit.py](https://github.com/Snowflake-Labs/sfguide-getting-started-with-image-classification-with-anthropic-snowflake-cortex/blob/main/image_analysis_streamlit.py) file
   * Click "Run" to launch your application

The application provides:
- A model selector dropdown (Claude 3.5 Sonnet or Pixtral-large)
- Analysis type selection
- Custom prompt capability
- Image selection and display
- Prompt display for transparency
- Results viewing

<!-- ------------------------ -->
## Conclusion And Resources

Duration: 5

Congratulations! You've successfully built an end-to-end image analysis application using AI models via Snowflake Cortex. This solution allows you to extract valuable insights from images, detect emotions, analyze scenes, and generate rich descriptions - all within the Snowflake environment.

To continue your learning journey, explore creating more advanced prompting techniques, building domain-specific image analysis systems, or integrating this capability with other Snowflake data workflows.

### What You Learned
- How to set up Snowflake for image storage and processing
- How to use AI models like Claude 3.5 Sonnet and Pixtral-large for multimodal analysis
- How to create custom prompts for specialized image analysis
- How to build a Streamlit application for interactive image analysis
- How to implement batch processing for multiple images

### Related Resources
- [Snowflake Cortex Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-llm-rest-api)
- [Anthropic Tool Use on Snowflake Cortex Quickstart](https://quickstarts.snowflake.com/guide/getting-started-with-tool-use-on-cortex-and-anthropic-claude/index.html?index=..%2F..index#0)
- [Anthropic RAG on Snowflake Cortex Quickstart](https://quickstarts.snowflake.com/guide/getting_started_with_anthropic_on_snowflake_cortex/index.html?index=..%2F..index#0)
