# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime
from pytz import timezone
from decouple import config, AutoConfig
import paramiko as pk

# activate virtual env
#conda activate .my_env
# Loading Credentials
# set the environment variables in the server from the .env file. Run this command in the folder in gitbash
# set -o allexport && source .env && set +o allexport

config = AutoConfig(search_path='.env')
USERNAME = config("USER_NAME")
PASSWORD = config("PASSWORD")
PORT=config("PORT")
LOCATION=config("LOCATION_CSCS")
IP_ADDRESS=config("IP_ADDRESS")
SPREADSHEET_ID=config("SPREADSHEET_ID")

#testing
print(f'Username: {USERNAME}, Password: {PASSWORD}, Port:{PORT}, IP_adress: {IP_ADDRESS}, SpreadsheetId:{SPREADSHEET_ID}')

def extract_gdrive(url, sheets):
    df_i = None
    df_p = None

    df_i = pd.read_excel(url, sheet_name = sheets[0])
    df_p = pd.read_excel(url, sheet_name = sheets[1])
    
    print(f"Extracted Inventory data of size (rows,cols): {df_i.shape}")
    print(f"Extracted Production data of size (rows,cols): {df_p.shape}")

    return df_i, df_p


def connection_open():
    ssh = None
    sftp_client = None
    try:
        ssh = pk.SSHClient()
        ssh.set_missing_host_key_policy(pk.AutoAddPolicy())
        ssh.connect(hostname=IP_ADDRESS, 
                    username=USERNAME,
                    password=PASSWORD,
                    port=PORT)
        sftp_client=ssh.open_sftp()
        print('SFTP Connection opened')
    except pk.AuthenticationException:
        print('ERROR : Authentication failed because of irrelevant details!')
    except:
        print(f'ERROR : Could not connect to {IP_ADDRESS}')
    return ssh, sftp_client

def connection_close(ssh, sftp_client):
    # Close the connections
    sftp_client.close()
    ssh.close()
    print('Connection Closed')
    return None
    

def trans_conn_load(df_i, df_p, desti_file_i, desti_file_p):
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
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=IP_ADDRESS, 
                username=USERNAME,
                password=PASSWORD,
                port=PORT)
    sftp_client=ssh.open_sftp()

    upload_file_path = f'/home/{USERNAME}/uploads'

    # get current working directory
    print('Connected to SFTP')

    # move to the uploads directory
    # sftp_client.chdir('./uploads')
    sftp_client.chdir(upload_file_path)
    print(f'Changed directory to {sftp_client.getcwd()} for upload')

    
    # put the df in the uploads directory
    with sftp_client.open(desti_file_i, "w") as f:
        df_i[cols_i].to_csv(f, sep=str('|'), index=False)
    print('Upload of Invertory File Complete')
    
    with sftp_client.open(desti_file_p, "w") as g:
        df_p[cols_p].to_csv(g, sep=str('|'), index=False)
    print('Upload of Production File Complete')

    # Close the connections
    sftp_client.close()
    ssh.close()
    print('Connection Closed')

def write_server(df_i, df_p, desti_file_i, desti_file_p, write_folder_server, sftp_client):
    
    # move to the uploads directory
    # sftp_client.chdir('./uploads')
    try:
        sftp_client.chdir(write_folder_server) #Test if remote path exists
        print(f'Changed directory to {sftp_client.getcwd()} for upload')
    except IOError:
        sftp_client.mkdir(write_folder_server) #Create remote path
        sftp_client.chdir(write_folder_server)
        print(f'Created & changed directory to {sftp_client.getcwd()} for upload')

    # put the df in the uploads directory
    with sftp_client.open(desti_file_i, "w") as f:
        df_i.to_csv(f, sep=str('|'), index=False)
    print(f'Upload of Invertory File of size (rows, cols) {df_i.shape} Complete')
    
    with sftp_client.open(desti_file_p, "w") as g:
        df_p.to_csv(g, sep=str('|'), index=False)
    print(f'Upload of Production File of size (rows, cols) {df_p.shape} Complete')

    return None


def write_local(df_i, df_p, desti_file_i, desti_file_p, write_folder_local):
    write_path_i = os.path.join(write_folder_local, desti_file_i)
    write_path_p = os.path.join(write_folder_local, desti_file_p)

    print(f'Writing inventory data of size (rows, cols) {df_i.shape} to {desti_file_i}')
    df_i[cols_i].to_csv(write_path_i, sep=str('|'), index=False)

    print(f'Writing production data of size (rows, cols) {df_p.shape} to {desti_file_p}')
    df_p[cols_p].to_csv(write_path_p, sep=str('|'), index=False)

# Extracting file from gdrive
# https://stackoverflow.com/questions/37243121/using-pandas-to-read-in-excel-file-from-url-xlrderror


if __name__ == "__main__":

        # run type setting
    write_type= ['local', 'server']
    write_selection = 0 # 0 for local & 1 for server

    
    #getting current cst date time
    central_tz = timezone('US/Central')
    date_frmt = '%Y%m%d_%H%M'
    my_date = datetime.now(central_tz).strftime(date_frmt)
    print(my_date)

    # local settings
    write_folder_local = 'data'

    #server settings
    write_folder_server = f'/home/{USERNAME}/uploads'
    

    # dataset settings
    url = f'https://drive.google.com/u/0/uc?id={SPREADSHEET_ID}&export=download'
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

    # TRANSFORMATION & LOAD
    if not [x for x in (df_i, df_p) if x is None]:
        if write_type[write_selection] == 'local':
            write_local(df_i[cols_i], df_p[cols_p], desti_file_i, desti_file_p, write_folder_local)
        else:
            ssh, sftp_client = connection_open()
            if not [x for x in (ssh, sftp_client) if x is None]:
                write_server(df_i[cols_i], df_p[cols_p], desti_file_i, desti_file_p, write_folder_server, sftp_client)
                connection_close(ssh, sftp_client)
            else:
                print('ERROR: Could not connect to Client Server!')
    else:
        print('No data available from the URL')
    
    #trans_conn_load(df_i, df_p, desti_file_i, desti_file_p)