import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from os import access
import requests
from pathlib import Path
import re

# Opens windows with python click through download instructions for every document

def main():
    for id in list_of_ids:
        driver = webdriver.Chrome(ChromeDriverManager().install())

        page_url =f"https://assistive.eboardsolutions.com/SB_Meetings/ViewMeeting.aspx?S=42&MID={id}"
        driver.get(page_url)

        wait = WebDriverWait(driver, 10)

        # Store the ID of the original window
        original_window = driver.current_window_handle
        assert len(driver.window_handles) == 1

        #Click on print button to get dropdown
        time.sleep(3)
        button = driver.find_element(By.CSS_SELECTOR, '[title="Print Options"]').click()

        #Click on "Print Minutes"
        print_button = driver.find_element(By.XPATH, '/html/body/form/div[12]/div[3]/div[2]/div[5]/div[2]/app-viewmeeting/app-app/app-viewmeeting/div[1]/app-header/div[2]/div/div[2]/div[2]/ul/li[2]/a').click()

        #Switch windows to new tab
        # Wait for the new window or tab
        wait.until(EC.number_of_windows_to_be(2))
        # Loop through until we find a new window handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break
        
        #Get url
        while "PrintMinutesSettings" in driver.current_url: 
            time.sleep(2)
        created_link = driver.current_url

        #Quit all windows
        driver.quit

        #Parsing link
        clean_link = re.split('fid=|&fname=', created_link)
        fid_string = clean_link[1]
        type_split = re.split('%20', clean_link[2])
        fname_string = " ".join(type_split)

        #Create query string
        querystring = {"fid":fid_string,"fname":fname_string}

        url = "https://app1.eboardsolutions.com//api/PrintMinutes/ViewPrintMinutes"

        payload = ""
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            'Accept-Language': "en-US,en;q=0.5",
            'Accept-Encoding': "gzip, deflate, br",
            'Connection': "keep-alive",
            'Cookie': "visid_incap_2280386=hbvDYqY0S1OkuIM2uczbGQ7dN2IAAAAAQUIPAAAAAAD772CDCzy85/n7j1EPaO0S; _ga=GA1.2.178823199.1647828242; ps_rvm_A7Bh=%7B%22pssid%22%3A%228UATVAvhwvUCnfpJ-1654551634173%22%2C%22last-visit%22%3A%221654551382245%22%7D; incap_ses_1424_2280386=FzWOBYNhRCJmG626yhDDEyRtnmIAAAAAEoIHBg+RFrWCb/u/v76AjQ==; dtCookie=v_4_srv_3_sn_3006221A37AF689E03360FD5EB5DE893_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_1; rxVisitor=1654549805979DLFT8SKNJUM2BTFKSGAP1UCHL52B8UPB; dtPC=3`-vNNKPCFOJCMUCHVGMKRCKCKFGHAJKKSDK-0e0; rxvt=1654553350948|1654549805983; dtLatC=6; dtSa=-; _gid=GA1.2.457053572.1654549818; nlbi_2280386=jY6SUry2Chech7l6eiFLeAAAAADz1Ypbz+0GhpzXCQYFDeRN",
            'Upgrade-Insecure-Requests': "1",
            'Sec-Fetch-Dest': "document",
            'Sec-Fetch-Mode': "navigate",
            'Sec-Fetch-Site': "none",
            'Sec-Fetch-User': "?1",
            'TE': "trailers"
            }

        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

        relative_filename = "".join(type_split)
        filename = Path(f"C:/Users/Cole Schnell/Desktop/Summer/Learn/project-2/CPS_files/{relative_filename}.pdf")

        filename.write_bytes(response.content)

        #Sleep before next request
        time.sleep(5)
    print("Task complete")

list_of_ids = ['10836', '10851', '10757', '10879', '10824', '10821', '10624', '10744', '10667', '10471', '10469', '10599', '10388', '10321', '10478', '10455', '10298', '10245',
'10327', '10090', '10214', '10056', '9969', '10106', '9965', '10082', '9910', '9857', '9856', '9825', '9926', '9674', '9747', '9585', '9511', '9588', '9445', 
'9495', '9360', '9482', '9280', '9253', '9252', '9349', '9309', '9185', '9239', '9143', '9235', '9133', '9194', '8927', '9063', '8885', '8802', '8821', '8909',
'8739', '8838', '8786', '8643', '8652', '8712', '8601', '8603', '8700', '8559', '8614', '8524', '8522', '8565', '8572', '8313', '8495', '8511', '8515', '8304',
'8489', '8473', '8447', '8290', '8348', '8206', '8258', '8053', '8205', '8125', '8124', '8010', '8009', '7753', '8051', '8011', '7966', '7969', '7840', '7961',
'7913', '7838', '7870', '7719', '7787', '7849', '7636', '7694', '7752', '7594', '7596', '7700', '7409', '7408', '7406', '7423', '7269', '7268', '7266', '7414',
'7208', '7294', '7207', '7179', '7178', '7254', '7170', '7099', '7019', '7119', '7163', '6984', '6935', '6932', '6959', '7017', '6726', '6783', '6744',
'6774', '6888', '6742', '6704', '6592', '6748', '6500', '6594', '6506', '6473', '6419', '6417', '6415', '6429', '6259', '6391', '6319', '6257', '6262', 
'6236', '6176', '6186', '6141', '6129', '6127', '6150', '6218', '6148', '5969', '6017', '5871', '5982', '6094', '5849', '5901', '5848', '5846', '5925', 
'5876', '5726', '5542', '5787', '5724', '5785', '5773', '5607', '5606', '5605', '5603', '5692', '5526', '5530', '5540', '5514', '5447', '5446', '5348', 
'5412', '5410', '5266', '5263', '5358', '5331', '5107', '5100', '5126', '4932', '4931', '5110', '4934', '4930', '5043', '5042', '4921', '4923', '4985', 
'4760', '4844', '4933', '4758', '4759', '4883', '4721', '4720', '4804', '4599', '4659', '4507', '4506', '4579', '4483', '4406', '4407', '4452', '4326',
'4380', '4296', '4230', '4254', '4229', '4180', '4091', '4173', '4004', '4075', '4003', '4133', '4005', '4020', '4018', '3955', 
'3977', '3806', '3905', '3929', '3939', '3805', '3678', '3817', '3819', '3677', '3702', '3701', '3738', '3700', '3637', '3558', '3494', '3455', '3583', '3456']

#267 ids

if __name__ == '__main__':
    main()