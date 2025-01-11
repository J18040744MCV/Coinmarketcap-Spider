from selenium import webdriver
import pandas as pd
import numpy as np
import time
from selenium.common.exceptions import NoSuchElementException
from platform import system
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from glob import glob

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)




class CoinsDataScraper:
    def __init__(self,
                 filter=None):

        self.filter = filter

        """
        спред в онлайне/количество подписчиков в телеге = скрапить

        """

        if system() == 'Windows':
            self.driver = webdriver.Chrome()
        elif system() == 'Linux':
            self.driver = webdriver.Chrome(executable_path = '/usr/lib/chromium-browser/chromedriver')

        self.driver_actions = ActionChains(self.driver)

        self.driver.get("https://coinmarketcap.com/")

        columns_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                               value="button.sc-7d96a92a-0:nth-child(2)")
        columns_ent.click()

        time.sleep(1)



        price_change_30d_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                                        value="div.sc-1c94022b-8:nth-child(2) > div:nth-child(2) > span:nth-child(4)")
        price_change_30d_ent.click()

        max_supply_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                                  value="div.sc-1c94022b-8:nth-child(5) > div:nth-child(2) > span:nth-child(3)")
        max_supply_ent.click()



        """
        Reject Cookies
        """


        try:

            cookies_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                                   value="#onetrust-reject-all-handler"
                                                   )
            cookies_ent.click()
        except Exception as e:
            print(f"{e} occured while trying to click on the cookies ent -> passing")
            pass

        """
        Moving ob
        """

        chart_7d_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                                value="div.sc-1c94022b-8:nth-child(6) > div:nth-child(2) > span:nth-child(2)")

        chart_7d_ent.click()



        apply_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                             value="button.jOyYlg:nth-child(2)")

        apply_ent.click()


        time.sleep(6)


        filter_variants = ["Category","Algorithm","Platform","Industry"]

        "/html/body/div/div/div[1]/div[2]/div/div[1]/ul/li[1]/div/span/button"
        "/html/body/div/div/div[1]/div[2]/div/div[1]/ul/li[4]/div/span/button"

        time.sleep(1)
        if self.filter:
            filters_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                                   value=".BaseButton_size-sm__oHKNE")
            filters_ent.click()
            time.sleep(1)
            filter_variant_ent = self.driver.find_element_by_xpath(f"/html/body/div/div/div[1]/div[2]/div/div[1]/ul/li[{filter_variants.index(self.filter[0])+1}]/div/span/button/span")

            filter_variant_ent.click()
            time.sleep(1)

            for l in self.filter[1]:
                self.driver_actions.send_keys(l).perform()
                time.sleep(0.1)

            time.sleep(1)

            self.driver_actions.send_keys(Keys.ENTER).perform()
            time.sleep(3)


        """НАЗВАНИЕ ТОЖЕ НУЖНО СКРАПИТЬ - СДЕЛАТЬ"""

    def get_coins_fundamentals(self):

        n_ent_on_page = 100

        tickers = []
        prices = []
        names = []
        daily_performance_pcnts = []
        weekly_performance_pcnts = []
        monthly_performance_pcnts = []
        market_caps = []
        vols_24h = []
        CircSups = []
        MaxSups = []


        y = 1000
        for timer in range(0, 8):
            self.driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 1000
            time.sleep(0.5)



        n_of_ents_ent = self.driver.find_element(by=By.CSS_SELECTOR,
                                                 value=".kmNipA")

        print("n_of_ents_ent.text = ", n_of_ents_ent.text)


        n_of_ents = n_of_ents_ent.text.split()[-1]
        n_of_pages = int(int(n_of_ents)/n_ent_on_page)+1


        print("n_of_ents = ", n_of_ents)
        print("n_of_pages = ", n_of_pages)



        for p in range(n_of_pages-1):


            if p > 0:
                y = 1000
                for timer in range(0, 8):
                    self.driver.execute_script("window.scrollTo(0, " + str(y) + ")")
                    y += 1000
                    time.sleep(0.75)

            for n in range(n_ent_on_page):
                while True:
                    try:

                        ticker_ent = self.driver.find_element(by=By.XPATH,
                                                              value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[3]/div/a/div/div/div/div/p")

                        ticker = ticker_ent.text
                        tickers.append(ticker)
                        print("ticker = ", ticker)
                        break
                    except NoSuchElementException:
                        self.driver.refresh()
                        self.driver.execute_script("window.scrollTo(0,0)")
                        y = 1000
                        for timer in range(0, 8):
                            self.driver.execute_script("window.scrollTo(0, " + str(y) + ")")
                            y += 1000
                            time.sleep(0.75)

                        pass

                try:

                    px_ent = self.driver.find_element(by=By.XPATH,
                                                      value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[4]/div/span")



                    px = px_ent.text
                    px = px.replace(',', '')

                    px = px.replace('$', '')
                    try:
                        px = float(px)
                    except ValueError:

                        px = px[1:]
                        try:
                            px = float(px)
                        except ValueError:
                            pass


                    prices.append(px)
                    print("px = ", px)
                except NoSuchElementException:
                    print(f"no px for {ticker}...")
                    prices.append(None)


                try:

                    name_ent = self.driver.find_element(by=By.XPATH,
                                                        value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[3]/div/a/div/div/div/p")

                    name = name_ent.text.split(" ")[0]
                    name = name.replace(',', '')
                    # name = float(name)
                    names.append(name)
                    print("name = ", name)
                except NoSuchElementException:
                    print(f"no name for {ticker}...")
                    names.append(None)





                try:

                    daily_performance_pcnt_ent = self.driver.find_element(by=By.XPATH,
                                                                          value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[6]/span")


                    daily_performance_pcnt_direction_ent = self.driver.find_element(by=By.XPATH,
                                                                                    value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[6]/span/span")

                    daily_performance_pcnt = daily_performance_pcnt_ent.text

                    daily_performance_pcnt = daily_performance_pcnt.replace('%', '')
                    daily_performance_pcnt = float(daily_performance_pcnt)
                    daily_performance_pcnt = daily_performance_pcnt*0.01


                    print("daily_performance_pcnt_ent.text = ", daily_performance_pcnt_ent.text)

                    daily_performance_direction_class_name = daily_performance_pcnt_direction_ent.get_attribute("class")

                    if daily_performance_direction_class_name == "icon-Caret-down":
                        daily_performance_pcnt = daily_performance_pcnt*-1
                    else:
                        pass

                    daily_performance_pcnts.append(daily_performance_pcnt)
                    print("daily_performance_pcnt = ", daily_performance_pcnt)

                except NoSuchElementException:
                    print(f"no daily_performance_pcnt for {ticker}...")
                    daily_performance_pcnts.append(None)






                try:


                    weekly_performance_pcnt_ent = self.driver.find_element(by=By.XPATH,
                                                                           value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[7]/span")

                    weekly_performance_pcnt_direction_ent = self.driver.find_element(by=By.XPATH,
                                                                                     value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[7]/span/span")

                    weekly_performance_pcnt = weekly_performance_pcnt_ent.text

                    weekly_performance_pcnt = weekly_performance_pcnt.replace('%', '')
                    weekly_performance_pcnt = float(weekly_performance_pcnt)
                    weekly_performance_pcnt = weekly_performance_pcnt*0.01

                    weekly_performance_direction_class_name = weekly_performance_pcnt_direction_ent.get_attribute("class")


                    if weekly_performance_direction_class_name == "icon-Caret-down":
                        weekly_performance_pcnt = weekly_performance_pcnt*-1
                    else:
                        pass

                    weekly_performance_pcnts.append(weekly_performance_pcnt)
                    print("weekly_performance_pcnt = ", weekly_performance_pcnt)


                except NoSuchElementException:
                    print(f"no weekly_performance_pcnt for {ticker}...")
                    weekly_performance_pcnts.append(None)





                try:
                    monthly_performance_pcnt_ent = self.driver.find_element(by=By.XPATH,
                                                                            value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[11]/span")

                    monthly_performance_pcnt_direction_ent = self.driver.find_element(by=By.XPATH,
                                                                                      value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[11]/span/span")

                    monthly_performance_pcnt = monthly_performance_pcnt_ent.text
                    monthly_performance_pcnt = monthly_performance_pcnt.replace('%', '')
                    monthly_performance_pcnt = float(monthly_performance_pcnt)
                    monthly_performance_pcnt = monthly_performance_pcnt*0.01
                    monthly_performance_pcnt_direction_class_name = monthly_performance_pcnt_direction_ent.get_attribute("class")
                    if monthly_performance_pcnt_direction_class_name == "icon-Caret-down":
                        monthly_performance_pcnt = monthly_performance_pcnt*-1
                    else:
                        pass
                    monthly_performance_pcnts.append(monthly_performance_pcnt)
                    print("monthly_performance_pcnt = ", monthly_performance_pcnt)
                except NoSuchElementException:
                    print(f"no monthly_performance_pcnt for {ticker}...")
                    monthly_performance_pcnts.append(None)





                try:
                    m_cap_ent = self.driver.find_element(by=By.XPATH,
                                                         value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[8]/p/span[2]")
                    m_cap = m_cap_ent.text
                    m_cap = m_cap.replace(',', '')
                    m_cap = m_cap.replace('$', '')
                    m_cap = int(m_cap)
                    market_caps.append(m_cap)
                    print("m_cap = ", m_cap)
                except NoSuchElementException:
                    print(f"no m_cap for {ticker}...")
                    market_caps.append(None)

                try:


                    vol_24h_ent = self.driver.find_element(by=By.XPATH,
                                                           value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[9]/div/a/p")
                                                           # value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[6]/span")



                    vol_24h = vol_24h_ent.text
                    vol_24h = vol_24h.replace(',', '')
                    vol_24h = vol_24h.replace('$', '')
                    # vol_24h = int(vol_24h)
                    vol_24h = float(vol_24h)
                    vols_24h.append(vol_24h)
                    print("vol_24h = ", vol_24h)
                except NoSuchElementException:
                    print(f"no vol_24h for {ticker}...")
                    vols_24h.append(None)


                try:
                    CircSup_ent = self.driver.find_element(by=By.XPATH,
                                                           value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[10]/div/div/p")




                    CircSup = CircSup_ent.text.split(" ")[0]
                    CircSup = CircSup.replace(',', '')
                    CircSup = float(CircSup)
                    CircSups.append(CircSup)
                    print("CircSup = ", CircSup)
                except NoSuchElementException:
                    print(f"no CircSup for {ticker}...")
                    CircSups.append(None)




                try:



                    MaxSup_ent = self.driver.find_element(by=By.XPATH,
                                                          value=f"/html/body/div[1]/div[2]/div[1]/div[2]/div/div[1]/div[5]/table/tbody/tr[{n+1}]/td[12]")





                    MaxSup = MaxSup_ent.text.split(" ")[0]
                    if MaxSup == "--":
                        raise NoSuchElementException
                    MaxSup = MaxSup.split(" ")[0]
                    MaxSup = MaxSup.replace(',', '')



                    MaxSup = float(MaxSup)
                    MaxSups.append(MaxSup)
                    print("MaxSup = ", MaxSup)
                except NoSuchElementException:
                    print(f"no MaxSup for {ticker}...")
                    MaxSups.append(None)

                print("\n")



            next_page_link = f"https://coinmarketcap.com/?page={p+2}"
            print("getting ", next_page_link)
            self.driver.get(next_page_link)
            time.sleep(8)

        """
        Сравнивать колонку тикеров со старой таблицой, дабы вычленить новые проекты, которые только попали на Coinmarketcap
        """


        # self.ml

        gb = glob("C:/SmartSynthetics/WORK/data/coins_fundamentals/cmc.None.data.*.xlsx")


        if len(gb) == 0:

            gb = glob("./cmc.None.data.*.xlsx")

            if len(gb) == 0:

                gb = "./cmc.None.data.v00.xlsx"

            else:
                gb = gb[-1]

        else:
            gb = gb[-1]



        path = gb.split(".")

        path[-2] = f"v{int(path[-2][1:]) + 1:02}"

        path = ".".join(path)


        coin_data_df = pd.DataFrame(data=[tickers,prices,names,daily_performance_pcnts,weekly_performance_pcnts,monthly_performance_pcnts,market_caps,vols_24h,CircSups,MaxSups]).T

        coin_data_df.columns = ["ticker", "price", "name", "daily_performance", "weekly_performance", "monthly_performance", "market_cap", "vol_24h","CircSups","MaxSups"]

        coin_data_df['market_cap'] = coin_data_df['market_cap'].replace(0, np.nan)

        coin_data_df["attention_SPREAD"] = coin_data_df["vol_24h"]/coin_data_df["market_cap"]


        coin_data_df.to_excel(path, index=False)

        print("coin_data_df = \n", coin_data_df)

        print("saved to = ", path)



if __name__ == "__main__":

    cds = CoinsDataScraper()

    cds.get_coins_fundamentals()


















