# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime
from pytz import timezone
from decouple import config, AutoConfig
import paramiko as pk
import functions_framework
import requests


def extract_gdrive(url, sheets):
    """Extracts sheets from Gdrive by specifying the url in the pandas read_excel function
    Args:
        url (str): the url of the spreadsheet which is the data source
        username (list): names of the sheets to be extracted
    Returns:
        df_i (pandas.dataframe): Pandas df containing inventory data
        df_p (pandas.dataframe): Pandas df containing production data
    """
    df_i = None
    df_p = None
    try:
        df_i = pd.read_excel(url, sheet_name = sheets[0])
        df_p = pd.read_excel(url, sheet_name = sheets[1])
    except Exception as e:
        print(f'Error: {e}! - File Extraction Failed')
        return None, None
    print(f"Extracted Inventory data of size (rows,cols): {df_i.shape}")
    print(f"Extracted Production data of size (rows,cols): {df_p.shape}")
    return df_i, df_p


def connection_open(ip_address, username, password, port):
    """Opens the ssh & sftp  connection to the server using Paramiko
    Args:
        ip_address (str): ip address of the server
        username (str): username to log into the server
        password (str): password for the username
        port (int): the port to connect to
    Returns:
        ssh (Paramiko.SSHClient) : contains the ssh connection to the server
        sftp_client (Paramiko.SFTPClient) : contains the sftp connection to the server
    """
    ssh = None
    sftp_client = None
    try:
        ssh = pk.SSHClient()
        ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
        ssh.connect(hostname=ip_address, 
                    username=username,
                    password=password,
                    port=port)
        sftp_client=ssh.open_sftp()
        print('SFTP Connection opened')
    except pk.AuthenticationException:
        print('ERROR : Authentication failed because of irrelevant details!')
    except Exception as e:
        print(f'ERROR: {e}')
    return ssh, sftp_client

def connection_close(ssh, sftp_client):
    """Closes the ssh & sftp  connection to the server
    Args:
        ssh (Paramiko.SSHClient) : contains the ssh connection to the server
        sftp_client (Paramiko.SFTPClient) : contains the sftp connection to the server
    Returns:
        None
    """
    # Close the connections
    sftp_client.close()
    ssh.close()
    print('Connection Closed')
    return None
    

def write_to_server(df_i, df_p, desti_file_i, desti_file_p, write_folder_server, sftp_client):
    """Writes the dataframes to the uploads folder on the client server as .txt files
    Args:
        df_i (pandas.dataframe): Pandas df containing inventory data
        df_p (pandas.dataframe): Pandas df containing production data
        desti_file_i (str): output file name for inventory data
        desti_file_p (str): output file name for production data
        write_folder_server (str): folder on the server to which the data needs to be written to
        sftp_client ( paramiko.SFTPClient) : contains the sftp connection to the server
    Returns:
        None
    """
    # move to the uploads directory
    # sftp_client.chdir('./uploads')
    try:
        sftp_client.chdir(write_folder_server) #Test if remote path exists
        print(f'Changed directory to {sftp_client.getcwd()} for upload')
    except IOError:
        #sftp_client.mkdir(write_folder_server) #Create remote path
        #sftp_client.chdir(write_folder_server)
        #print(f'Created & changed directory to {sftp_client.getcwd()} for upload')
        print('ERROR_NOTE:Uploads folder not avialable - Failed to upload files!!')
        return None

    # put the df in the uploads directory
    with sftp_client.open(desti_file_i, "w") as f:
        df_i.to_csv(f, sep=str('|'), index=False)
    print(f'Upload of Invertory File of size (rows, cols) {df_i.shape} Complete')
    
    with sftp_client.open(desti_file_p, "w") as g:
        df_p.to_csv(g, sep=str('|'), index=False)
    print(f'Upload of Production File of size (rows, cols) {df_p.shape} Complete')

    return None


def write_local(df_i, df_p, desti_file_i, desti_file_p, write_folder_local):
    """Writes the dataframes to the data folder on the local system
    Args:
        df_i (pandas.dataframe): Pandas df containing inventory data
        df_p (pandas.dataframe): Pandas df containing production data
        desti_file_i (str): output file name for inventory data
        desti_file_p (str): output file name for production data
        write_folder_local (str): local data folder to which the data needs to be written to
    Returns:
        None
    """
    write_path_i = os.path.join(write_folder_local, desti_file_i)
    write_path_p = os.path.join(write_folder_local, desti_file_p)

    print(f'Writing inventory data of size (rows, cols) {df_i.shape} to {desti_file_i}')
    df_i.to_csv(write_path_i, sep=str('|'), index=False)

    print(f'Writing production data of size (rows, cols) {df_p.shape} to {desti_file_p}')
    df_p.to_csv(write_path_p, sep=str('|'), index=False)

    return None



def etl(request):
    """Responds to any HTTP request and runs the code to perform ETL
       Extracts spreadsheet form Googlesheets on GDrive
       Transforms & Loads the data either to local data folder or to the server
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text indicating if ETL of data was successfull or not.
    """
    print(f'Value of requests passed to etl() {request} and type is {type(request)}')
    write_server = 1
    
    env_var = os.environ 
    username = env_var.get("USER_NAME_CSCS", "Specified environment variable is not set.")
    password = env_var.get("PASSWORD_CSCS", "Specified environment variable is not set.")
    port = env_var.get("PORT_CSCS", "Specified environment variable is not set.")
    ip_address = env_var.get("IP_ADDRESS_CSCS", "Specified environment variable is not set.")
    spreadsheet_id = env_var.get("SPREADSHEET_ID", "Specified environment variable is not set.")

    #testing
    print(f'Username: {username}, Password: {password}, Port:{port}, IP_adress: {ip_address}, SpreadsheetId:{spreadsheet_id}')
    
    
    if request in ['0', '1']:
        write_server = int(request)
    else:
        request_json = request.get_json(force=True, silent=True, cache=True)  
        # see https://flask.palletsprojects.com/en/2.0.x/api/ get_json Parse data as JSON
        #in v.2.1 of the Flask framework they changed the impl of the get_json and if the content type if not provided it returns http 400 - BAD Requests, therefore we are usong now force=true and silent=true
        if request.args and 'message' in request.args:
            write_server = int(request.args.get('message'))
        elif request_json and 'message' in request_json:
            write_server = int(request_json['message'])
    
    print(f'Value of write_server set to {write_server} and type is {type(write_server)}')

    #getting current cst date time
    central_tz = timezone('US/Central')
    date_frmt = '%Y%m%d_%H%M'
    my_date = datetime.now(central_tz).strftime(date_frmt)
    print(my_date)


    # dataset settings
    url = f'https://drive.google.com/u/0/uc?id={spreadsheet_id}&export=download'
    sheets = ['Aquasource_inventory', 'Aquasource_production']
    
    # Creating list of column names to preserve the order of the columns
    cols_i = ['FileCreationDate', 
                'FileCreationTime', 
                'Brand', 
                'LocationID', 
                'LocationName', 
                'InventoryDate', 
                'InventoryTime', 
                'DCItemNumber', 
                'ExclusiveIndicator', 
                'CatchWeightIndicator', 
                'ItemName', 
                'ItemDescription', 
                'ItemPriceperUOM', 
                'ItemPriceUOM', 
                'BrandItemNumber', 
                'ItemCasePackQuantity', 
                'ItemCasePackQuantityUOM', 
                'ManufacturerItemNumber', 
                'ManufacturerItemDescription', 
                'ManufacturerName', 
                'ManufacturerID', 
                'ManufacturerGLN', 
                'QuantityOnHand', 
                'InventoryUOM', 
                'QuantityOnHandinCases', 
                'QuantityOnHandinPounds', 
                'QuantityShipped', 
                'QuantityAvailable', 
                'QuantityCommitted', 
                'QuantityOnHold', 
                'QuantityWIP', 
                'UniqueRawIngredientValue', 
                'QuantityNextDaySales', 
                'QuantityonOrder', 
                'QuantityReceived', 
                'QuantityReturned', 
                'QuantitySold', 
                'QuantityWarehouseAdjustments', 
                'ShelfLifeDaysRemaining', 
                'NumberofPricingUOMperInventoryUOM', 
                'NumberofInventoryUOMperCustomerInvoiceUOM', 
                'LotNumber ', 
                'ProductionDate',
                'ExpirationDate', 
                'S1ProductionReceiptQuantity', 
                'S1ProductionReceiptDate', 
                'S2ProductionReceiptQuantity', 
                'S2ProductionReceiptDate', 
                'S3ProductionReceiptQuantity', 
                'S3ProductionReceiptDate']
    cols_p = ['FileCreationDate', 
              'FileCreationTime', 
              'Brand', 
              'LocationID',
              'LocationName', 
              'InventoryDate', 
              'InventoryTime', 
              'ItemName',
              'ItemCasePackQuantity',
              'ItemCasePackQuantityUOM',
              'ManufacturerItemNumber', 
              'ManufacturerItemDescription',
              'ManufacturerName', 
              'InventoryUOM', 
              'LotNumber', 
              'ProductionDate',
              'ProductionQuantity', 
              'FreezerInboundDate', 
              'FreezerInboundQuantity']
    
    # file name format = supplier_name_suppinv_YYYYMMDD_HHmm
    desti_file_i = f"TEST_supplier_name_suppinv_{my_date}.txt"
    desti_file_p = f"TEST_supplier_name_suppprod_{my_date}.txt"

    # EXTRACTION
    df_i, df_p = extract_gdrive(url, sheets)
    #df_i, df_p = None, None
    

    # TRANSFORMATION & LOAD
    if not [x for x in (df_i, df_p) if x is None]:
        if write_server == 0:
            # local settings
            print('NOTE: Writing data locally')
            write_folder_local = 'data'
            write_local(df_i[cols_i], df_p[cols_p], desti_file_i, desti_file_p, write_folder_local)
            print('SUCCESS: Files written to local data folder!')
            return 'SUCCESS: Files written to local data folder'
        else:
            #server settings
            write_folder_server = f'/home/{username}/uploads'
            ssh, sftp_client = connection_open(ip_address, username, password, port)
            if not [x for x in (ssh, sftp_client) if x is None]:
                write_to_server(df_i[cols_i], df_p[cols_p], desti_file_i, desti_file_p, write_folder_server, sftp_client)
                connection_close(ssh, sftp_client)
                print('SUCCESS: Files uploaded to server!')
                return 'SUCCESS: Files uploaded to server!'
            else:
                print('ERROR_NOTE: Could not connect to Client Server!')
                return 'ERROR_NOTE: Could not connect to Client Server!'
    else:
        print('ERROR_NOTE:Data Extraction Failed, spreadsheet unavailable!')
        return 'ERROR_NOTE:Data Extraction Failed, spreadsheet unavailable!'

def main(write_server: int=1):
    # 0 to write to local folder & 
    # 1 to write to the server

    etl(write_server)

if __name__ == "__main__":
    """Calls the etl from the main function to run the etl locally
    Args:
        write_selection (int): selection to indicate where to write the output local or server
    Returns:
        None
    Note:
    - Loading Credentials Locally
    - set the environment variables in the server from the .env file. Run this command in the folder in gitbash
    - set -o allexport && source .env && set +o allexport
    - use below to run the etl function by invoking via http
    - functions-framework --target hello --debug --port 8080 
    """
    import argparse
    parser = argparse.ArgumentParser(description='ETL Pipeline to pull data from Gdrive and write Client Server or Locally\n \
                                     You are running the ETL Pipeline from local system now \
                                     Options to Enter:\n \
                                     0-To write Locally \n \
                                     1-To write to the server\
                                     NOTE: The DEFAULT is 1')
    parser.add_argument('--write_server', metavar='int', required=False, nargs='?', const=1,
                        help='Enter 0 or 1')
    args = parser.parse_args()
    main(write_server=args.write_server)
