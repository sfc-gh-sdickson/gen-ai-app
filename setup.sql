USE ROLE accountadmin;
USE WAREHOUSE compute_wh;

CREATE DATABASE IF NOT EXISTS AI209_db;

-- Optional: Rename Database
// ALTER DATABASE multimodal_db RENAME TO AI209_db;

USE SCHEMA public;
    
-- Create an internal stage
CREATE OR REPLACE STAGE images_stage
    DIRECTORY = ( ENABLE = true )
    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' )
;
