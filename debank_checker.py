import time
import math
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


start_time = time.time()

options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
total_sum = 0
with open("addresses.txt", 'r') as file:
    line_counter = 0
    df = pd.DataFrame([], columns=['Token', 'Price', 'Native', 'Dollars', 'Chain', 'Total', 'Wallet'])
    for wallet in file:
        url = f"https://debank.com/profile/{wallet}"
        driver.get(url)
        time.sleep(10)

        tokens = driver.find_elements(By.CLASS_NAME, "db-table-cell") # Price, AssetAmt, Dollars
        chain = driver.find_elements(
            By.CLASS_NAME, "TokenWallet_detailLink__282Ky") # Token
        total = driver.find_elements(
            By.CLASS_NAME, "ProjectCell_assetsItemWorth__o2_hJ")

        line = []
        flag = 0
        df_print = pd.DataFrame([], columns=['Token', 'Price', 'Native', 'Dollars', 'Chain', 'Total', 'Wallet'])
        for index, elem in enumerate(tokens):
            Total = total[0].text if index == 4 else '--||--'
            total_sum += int(Total[1:]) if Total.startswith('$') else 0
            if index > 1 and index % 4 == 0:
                link_list = (chain[math.floor(index / 4) - 1].get_attribute('href')).split('/')
                Chain = link_list[4]
                line.extend([Chain, Total, line_counter])
                index = 1 if line[3][0] == '$' else 2
                Dollars = float(line[3][index:].replace(',', ''))
                if Dollars > 10:
                    line[-1] = line_counter if flag == 0 else '--||--'
                    flag = 1
                    df_print.loc[len(df_print)] = line
                line = list(map(lambda x: x.replace('$', '') if type(x) == str else x, line))
                line = list(map(lambda x: x.replace('<', '') if type(x) == str else x, line))
                df.loc[len(df)] = line
                line = []
            line.append(elem.text)
        line_counter += 1
        print(df_print.to_string(index=False) + '\n')
    print(f"Treasure: ${total_sum}")
    with open("df_test.csv", 'w') as file:
        file.write(df.to_csv())

end_time = time.time()
print(end_time - start_time)
driver.quit()
