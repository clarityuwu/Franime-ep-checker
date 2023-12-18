import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import TimeoutException

urls = input("Entrer l'url de la série de la ou tu veux commencer la vérification: ").split(',')
player = input("Sélectionne le player que tu veux vérifier (SENDVID ou SIBNET): ")
driver = webdriver.Firefox()

for url in urls:
    url = url.strip()
    driver.get(url)
    wait = WebDriverWait(driver, 2)

    while True:
        try:
            popup_content = wait.until(EC.presence_of_element_located((By.ID, "popupContent")))
            if popup_content:
                close_button = wait.until(EC.element_to_be_clickable((By.ID, "closeBtn")))
                close_button.click()
        except:
            pass

        dropdown_button = wait.until(EC.presence_of_element_located((By.ID, "headlessui-listbox-button-:r0:")))
        dropdown_button.click()
        players = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']//li")))
        players_text = [player.text for player in players]

        if 'Lecteur INDISPONIBLE' in players_text and ('Lecteur SENDVID' in players_text or 'Lecteur SIBNET' in players_text):
            pass
        elif 'Lecteur S22' in players_text and ('Lecteur SENDVID' in players_text or 'Lecteur SIBNET' in players_text):
            pass
        else :
            try:
                season = re.search(r's=(\d+)', driver.current_url).group(1)
                episode = re.search(r'ep=(\d+)', driver.current_url).group(1)
                anime_name = re.search(r'franime.fr/anime/(.*?)\?', driver.current_url).group(1)
                with open('errors.txt', 'a') as f:
                    f.write(f"Error: Aucun Lecteur Disponible. Anime: {anime_name}, Saison: {season}, Episode: {episode}\n")
                next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//p[text()='Épisode suivant' or text()='Saison suivante']]")))
                button_text = next_button.text
                if button_text == "Saison suivante":
                    next_button.click()
                else:
                    background_color = driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor;", next_button)
                    rgb_color = tuple(map(int, background_color[4:-1].split(',')))
                    if rgb_color == (23, 25, 31):
                        print("It's finished")
                        break  
                    else:
                        next_button.click()
                        continue
            except:
                pass
        
        if player.upper() == "SENDVID":
            player_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[contains(., 'Lecteur SENDVID')]")))
        elif player.upper() == "SIBNET":
            player_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//li[contains(., 'Lecteur SIBNET')]")))
        else:
            print("Invalid player selected")
            driver.close()
            exit()

        player_element.click()

        watch_episode_button = wait.until(EC.element_to_be_clickable((By.ID, "play_button")))
        watch_episode_button.click()
        time.sleep(1)

        if player.upper() == "SENDVID":
            try:
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'aspect-video flex w-full')]")))
                driver.switch_to.frame(iframe)
                try:
                    error_message = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'No compatible source was found for this media.')]")))
                    if error_message:
                        season = re.search(r's=(\d+)', driver.current_url).group(1)
                        episode = re.search(r'ep=(\d+)', driver.current_url).group(1)
                        anime_name = re.search(r'franime.fr/anime/(.*?)\?', driver.current_url).group(1)
                        with open('errors.txt', 'a') as f:
                            f.write(f"Error: Video Error. Anime: {anime_name}, Saison: {season}, Episode: {episode}\n")
                except TimeoutException:
                    season = re.search(r's=(\d+)', driver.current_url).group(1)
                    episode = re.search(r'ep=(\d+)', driver.current_url).group(1)
                    anime_name = re.search(r'franime.fr/anime/(.*?)\?', driver.current_url).group(1)
                    with open('errors.txt', 'a') as f:
                        f.write(f"Error: Cross Origin Error. Anime: {anime_name}, Saison: {season}, Episode: {episode}\n")
            except:
                pass

        if player.upper() == "SIBNET":
            try:
                iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@class, 'aspect-video flex w-full')]")))
                driver.switch_to.frame(iframe)

                error_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='videostatus']/p[text()='Видео недоступно.']")))
                if error_message:
                    season = re.search(r's=(\d+)', driver.current_url).group(1)
                    episode = re.search(r'ep=(\d+)', driver.current_url).group(1)
                    anime_name = re.search(r'franime.fr/anime/(.*?)\?', driver.current_url).group(1)
                    with open('errors.txt', 'a') as f:
                        f.write(f"Error: Lien Down. Anime: {anime_name}, Saison: {season}, Episode: {episode}\n")
            except:
                pass

        driver.switch_to.default_content()
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//p[text()='Épisode suivant' or text()='Saison suivante']]")))
        button_text = next_button.text
        if button_text == "Saison suivante":
            next_button.click()
        else:
            background_color = driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor;", next_button)
            rgb_color = tuple(map(int, background_color[4:-1].split(',')))
            if rgb_color == (23, 25, 31):
                print("It's finished")
                break  
            else:
                next_button.click()
driver.close()
