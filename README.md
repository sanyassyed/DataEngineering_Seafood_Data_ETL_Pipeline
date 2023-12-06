# SeafoodProject
<p> This project is to build an ETL pipeline to do the following</p>

* Extract data from ZOHO via API
* Transform the data
    - Read the `.xml` file
    - Add the required columns
    - Convert the data to `.txt` file with the following conditions
        1. Pipe character delimited ` | `
        1. Columns must be in order and contain no spaces
        1. Must Include Carriage Return (CR) & Line Feed (LF) syntax
* Load the data to client server via SFTP
* Schedule the above ETL to execute everyday