# Documentation
Find here the steps taken to create the project

* Created a project repository on GitHub `SeafoodProject`
* Used Codespace to execute the project
* Started work on creating the python code to transform the data
* Moving work to local machine
    * Steps to clone repo on local system
        1. Create a ssh key on the local system to connect to the GitHub repo as follows [More Info Here](https://github.com/xyzssyed/sf_eviction/blob/master/docs/README_Dev.md)
            ```bash
                xyz@pc MINGW64 /d/Documents
                $ ssh-keygen -t rsa
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
                xyz@pc MINGW64 /d/Documents
                $ cd /c/Users/xyz/.ssh/

                xyz@pc MINGW64 ~/.ssh
                $ ls
                id_rsa  id_rsa.pub

                xyz@pc MINGW64 ~/.ssh
                $ nano config

                # and write the below to file [Ctrl + O + Enter to save, Ctrl+X to exit]
                # write the path to the key from the root ~ and not /home
                    Host github.com
                        User git
                        IdentityFile ~/.ssh/id_rsa

            ```
        1. Add the public key generated to GitHub

        1. Clone the poject repo in the Documents folder
            ```bash
               xyz@pc MINGW64 ~/.ssh
                $ cd /d/Documents/

                xyz@pc MINGW64 /d/Documents
                $ git clone git@github.com:xyz/SeafoodProject.git
                Cloning into 'SeafoodProject'...
            ```
        1. Test if you are above to push to the repo
            ```bash
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

        1. If not; set the global config as follows
        ```bash
            # set the global variables
            git config --global user.email "xyz@gmail.com"
            git config --global user.name "xyz pc"
        ```
    * Add .gitignore file as follows
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
    