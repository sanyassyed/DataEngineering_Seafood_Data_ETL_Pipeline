# -*- coding: utf-8 -*-
import pandas as pd
import os
from datetime import datetime
from pytz import timezone
from decouple import config, AutoConfig
import paramiko
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
print(USERNAME)
print(PASSWORD)
print(PORT)
print(LOCATION)
print(IP_ADDRESS)
print(SPREADSHEET_ID)


central_tz = timezone('US/Central')
date_frmt = '%Y%m%d_%H%M'
my_date = datetime.now(central_tz).strftime(date_frmt)
print(my_date)

def connect_load(df_i, df_p, desti_file_i, desti_file_p):
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

# Extracting file from gdrive
# https://stackoverflow.com/questions/37243121/using-pandas-to-read-in-excel-file-from-url-xlrderror

def extract_gdrive(url, sheets):

    df_i = pd.read_excel(url, sheet_name = sheets[0])
    df_p = pd.read_excel(url, sheet_name = sheets[1])
    
    print(f"Extracted Inventory data of size (rows,cols): {df_i.shape}")
    print(f"Extracted Production data of size (rows,cols): {df_p.shape}")

    return df_i, df_p



def extract_local(data_dir, source_file, sheets):
    file_loc = os.path.join(data_dir, source_file)
    df_i = pd.read_excel(file_loc, sheet_name = sheets[0])
    df_p = pd.read_excel(file_loc, sheet_name = sheets[1])
    
    print(f"Extracted Inventory data of size (rows,cols): {df_i.shape}")
    print(f"Extracted Production data of size (rows,cols): {df_p.shape}")
    
    # testing
    #print(df_i.head())
    #print(df_p.head())
    #print(df_i.columns)
    #print(df_p.columns)
    #print(df_i.dtypes)

    return df_i, df_p

def transf_write_local(df_i, df_p, desti_file_i, desti_file_p) -> None:
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
    
    print(f'Writing inventory data of size (rows, cols) {df_i[cols_i].shape} to {desti_file_i}')
    df_i[cols_i].to_csv(desti_file_i, sep=str('|'), index=False)
    # df_i[cols_i].to_csv(desti_file_i, sep=str('|'), lineterminator= '\r\n', index=False)

    print(f'Writing production data of size (rows, cols) {df_p[cols_p].shape} to {desti_file_p}')
    df_p[cols_p].to_csv(desti_file_p, sep=str('|'), index=False)
    
    
    return None

def load() -> None:
    return None

if __name__ == "__main__":
    # file name format = supplier_name_suppinv_YYYYMMDD_HHmm
    #source_file = "AquaSource_Inventory_Production_Data.xlsx"
    sheets = ['Aquasource_inventory', 'Aquasource_production']
    url = f'https://drive.google.com/u/0/uc?id={SPREADSHEET_ID}&export=download'
    
    desti_file_i = f"TEST_supplier_name_suppinv_{my_date}.txt"
    desti_file_p = f"TEST_supplier_name_suppprod_{my_date}.txt"

    df_i, df_p = extract_gdrive(url, sheets)
    #df_i, df_p = extract_local(data_dir, source_file, sheets)
    
    #transf_write_local(df_i, df_p, desti_file_i, desti_file_p)
    connect_load(df_i, df_p, desti_file_i, desti_file_p)