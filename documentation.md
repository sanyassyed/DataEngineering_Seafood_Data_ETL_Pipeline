# Documentation
Find here the steps taken to create the project
## Initial Setup
### Git
* Created a project repository on GitHub `SeafoodProject`
* Used Codespace to execute the project
* Started work on creating the python code to transform the data

### Local System
* Moving work to local machine
    
    * Steps to clone repo on local system
        
        1. Create a ssh key on the local system to connect to the GitHub repo as follows [More Info Here](https://github.com/xyzssyed/sf_eviction/blob/master/docs/README_Dev.md)
            ```bash
                # Generate SSH-Key
                ssh-keygen -t rsa
                Generating public/private rsa key pair.
                Enter file in which to save the key (/c/Users/xyz/.ssh/id_rsa):
                Created directory '/c/Users/xyz/.ssh'.
                Enter passphrase (empty for no passphrase):
                Enter same passphrase again:
                Your identification has been saved in /c/Users/xyz/.ssh/id_rsa
                Your public key has been saved in /c/Users/xyz/.ssh/id_rsa.pub
                The key fingerprint is:
                *****
                *****
            ```
        1. Add a config file to .ssh folder as follows
            ```bash
                # Goto .ssh directory
                cd /c/Users/xyz/.ssh/
                # Check if keys are created
                ls
                id_rsa  id_rsa.pub
                # Create config file
                nano config
                # write the below to file [NOTE: Ctrl + O + Enter to save, Ctrl+X to exit]
                # write the path to the key from the root ~ and not /home
                    Host github.com
                        User git
                        IdentityFile ~/.ssh/id_rsa

            ```
        1. Add the public key generated to GitHub

        1. Clone the poject repo in the Documents folder
            ```bash
                # Goto root folder for project
               cd /d/Documents/
               git clone git@github.com:xyz/SeafoodProject.git
               Cloning into 'SeafoodProject'...
            ```
        1. Test if you are above to push to the repo
            ```bash
                # Goto project folder
                cd SeafoodProject
                # check the remote origin is set with ssh
                git remote -v
                # Check the SSH connection with repo from VM using
                ssh -T git@github.com
            ```
        
        1. Check if the global user.name & user.email has been set
        ```bash
            git config --list 
        ```

        7. If not; set the global config as follows
        ```bash
            # set the global variables
            git config --global user.email "xyz@gmail.com"
            git config --global user.name "xyz pc"
        ```

        8. Add .gitignore file as follows
        ```bash
            nano .gitignore
            # add enter the files to be ignored

        ``` 
    * Create a virtual conda environment to work on the project
        1. Open Gitbash
        1. Initialize conda for Git Bash as follows to view base conda environment
        ```bash 
            cd /d/Documents/SeafoodProject
            # initialize conda for gitbash as follows
            conda init bash
            # close the terminal and reopen it you should now see (base)
        ```
        1.  Create the virtual environment as follows:
        ```bash
            # Path to install the virtual env in the current project directory with python 3.10 and pip
            conda create --prefix ./.my_env python=3.10.9 pip 
        ```
        1.  Activate the virtual env  as follows
        ```bash
            conda activate .my_env 
            # to de-activate the virtual env my_env use the below 
            conda activate 
            # don't use deactivate just use activate to go to base
        ```
    * Install the required packages using pip
        ```bash
            # Check packages intalled already
            pip list
            # Install pandas, datetime, pytz
            pip install pandas datetime pytz

        ```

## Data Extraction
* Data was moved to Google Spreadsheets
* Data was extracted directly from GDrive by setting the Googlesheets permission to `View` for `Anyine with Link` [Source](https://stackoverflow.com/questions/37243121/using-pandas-to-read-in-excel-file-from-url-xlrderror)
* Using the document_id the google spreadsheet was extracted.


## Data Transformation
* The data validation was performed at the Google Spreadsheet level E.g. Calculating the `ShelfLifeDaysRemaining` from the value in the column `ExpirationDate`. Value is 0 if Expiration Date is crossed
* Transformation in the code: The column names that were required and their order was preserved

## Data Loading
Testing file upload to remote server. This involves the following steps

1. Create a remote server /instance: 
    * If using the oracle learning platform, create instance by uploading the public key on the system
        * [How to create account for Oracle Learning in Luna Lab](https://youtu.be/HOB5dhbcAyo?si=YtRMN-pLgoYRaa3n)
        * [Course with Lab](https://luna.oracle.com/lab/facec73e-8517-4314-877f-d4f8f429c5ab/steps)
        * [DTC Zoomcamp Video to create & log into instance on GCP](https://youtu.be/ae-CV2KfoN0?si=5jR9D7vydv3_YUVZ)

    * Then use the system terminal to log into the instance just created as follows
        ```bash
            # find the username for the instance created by clicking on the instance name in the dashboard and scrolling down to 'Instance Access' info
            ssh -i /home/luna.user/.ssh/id_rsa opc@external_ip 
        ```
    * Now you are in the server of the instace just created logged in as opc user
    * Create a new user named user1 with a password as follows [Source:Manage users on Linux](https://youtu.be/19WOD84JFxA?si=tNLPzMmHFXEflJjQ)
        ```bash
            # creates user named user1 with a home directory
            sudo useradd -m user1
            # creates a password for the user1
            sudo passwd user1
            # check if user is created
            grep user1 /etc/passwd  
            # check if passwd is created for the user1
            grep user1 /etc/shadow 
        ```
    * Now change the privilages for user1 to be able to log into the server via ssh using password and not key [Source](https://www.youtube.com/watch?v=9jC2JyLQZbk)
        ```bash
            # open the ssh config file in admin mode
            sudo nano /etc/ssh/sshd_config
            # Comment or uncomment the following line in the file
            
            PermitRootLogin yes
            #AuthorizedKeyFile .ssh/suthorized_keys .ssh/authorized_keys2
            #PasswordAuthentication no
            PasswordAuthentication yes
            Subsystem sftp  internal-sftp
            # Ctrl + O & Ctrl + X (for save and exit)
            # restart the sshd
            sudo systemctl restart sshd
        ```
    * You can now log into the remote server by using the username and password just created as follows via ssh
        ```bash
            # option 1 without specifying the port number, default for ssh is 22
            ssh user1@external_ip 
            # option 2
            ssh -p 22 user1@external_ip
            # it will as for password which you can enter when prompted
        ```
    
    1. Create a folder named `uploads` in the root directory 
        ```bash
            mkdir uploads
            # the absolute path of this directory is /home/user1/uploads
        ```

    1. Credentials if logging in via sftp in python
        * USERNAME=user1
        * PASSWORD=password
        * PORT=22
        * HOST=external_ip

    
    1. Upload file/folder to remote server via SFTP using python. [Video Source](https://www.youtube.com/watch?v=IQh0K_6ecrU&t=424s)

    1. Upload the pandas dataframe as a txt directly to the sever via sftp

    ## Deployment to Google Cloud Functions
    * The code had to refractored to do the following
        - Run on the local system for testing
        - Run on Google Cloud Functions when trigerred by http which require installing the functions framework as follows `pip install functions-framework==3.5.0`
    
    * The code was restructured with the following components
        - `main.py` : the file with the function etl() which would run the entire ETL process . 
            - If main.py was invoked the etl would write locally. Commands used `python main.py`
            - If etl() function was invoked via http it would write to the server `functions-framework --target hello --debug --port 8080 `
        - `requirements.txt`` : contained the packages required for the project which was generated using the `pipreqs`` package as follows
            ```bash
            pip install pipreqs
            pipreqs . --ignore ".my_env" 
            ```
        - `Envirinment Variables/Credentials`: These were used in the code by using the `os` package and set
            - Locally by using `set -o allexport && source .env && set +o allexport` command
            - On Google Cloud Functions by setting the `environemnt variable` via the Gloud UI

    * Google Cloud Functions Resources
        - [Google Cloud Functions examples for Python](https://cloud.google.com/functions/docs/samples?language=python)
        - [Google Cloud Functions basics video](https://www.youtube.com/watch?v=hnqeYOYDRYY&t=2986s)
        - [Configuring Environment Variables](https://cloud.google.com/functions/docs/configuring/env-var#google-cloud-console-ui_2)
        - [Configuring Secrets](https://cloud.google.com/functions/docs/configuring/secrets)
        - [Setting Google Cloud Function Locally For Testing - Example](https://dev.to/bornfightcompany/testing-cloud-functions-with-functions-framework-in-python-9cf)
        - [Setting secrets example](https://medium.com/google-cloud/managing-secrets-for-gcp-cloud-functions-844a56c8a820)
    
    ## Setting up Cloud Functions From GitHub
    1. Connect `GitHub` to `Cloud Source Repository` by following directions from [here](https://cloud.google.com/source-repositories/docs/mirroring-a-github-repository)
    2. Setting up `Cloud Functions` by pulling code from `Cloud Source Repository` by following directions from [here](https://cloud.google.com/functions/docs/deploy)
    
    ## Use Secrets Instead of Environment Variables
    * Follow directions [here](https://cloud.google.com/functions/docs/configuring/secrets) to 
        1. to create the secrets
        2. add the secrets as environment variables
    
    ## Create VM on GCP
    * Log into the vm from your local PC after adding the public key to `METADATA` using the command `ssh -i ~/.ssh/id_rsa sanya@external_ip`
    * Follow the steps in [here](#data-loading) to create a user on the VM

    ## NOTE:
    * When performing data entry remember to read the `DATA ENTRY INSTRUCTIONS` sheet first
    * Always remember to enter the mandatory fields
    * `ShelfLifeDaysRemaining` value is 0 if `ExpirationDate` is crossed
    * During testing do not pull the data from the Googlesheets URL continuously as it will lead to `403: Forbidden` Error as there is a usage limit per 100 seconds
    * When running the code locally remeber to:
        - use the GitBash terminal in VSCode
        - activate the project virtual env using `conda activate .my_env`
        - check if all the enviroment variables in the file `.env` have the right values
        - set the environment variables using `set -o allexport && source .env && +o allexport`
        - check the mode in the transform.py file if it is `local` or `server`
        - run the code as `python transform.py`
    * Running the project
        - Activate the virtual environment `conda activate .my_env`
        - Set the environment variables from the .env file with the credentials to connect to the server. Run the following command in the project folder in gitbash terminal `set -o allexport && source .env && set +o allexport`
        - `Locally for testing without Functions Framework and running via main() function`
            * To write to local data folder `python main.py --write_server=0`
            * To write to server `python main.py` or `python main.py --write_server=1`
        - `Locally for testing with Functions Framework to invoke via http the etl() function`
            * Run the command `functions-framework --target etl --debug --port 8080`
            * To write to local data folder goto web browser & copy paste `http://192.168.0.38:8080/?message=0` message here could be of value 0 to write to local data folder and 1 to write to server
            4. To write to server `http://192.168.0.38:8080` or `http://192.168.0.38:8080/?message=1`

  


