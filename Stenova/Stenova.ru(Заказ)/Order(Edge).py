from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# 1. Авторизация
driver = webdriver.Edge()
driver.implicitly_wait(10)
driver.get("https://www.stenova.ru/login/")
driver.maximize_window()

# Ввод email
driver.find_element(By.NAME, "USER_LOGIN").send_keys("san----95@mail.ru")

# Ввод пароля
driver.find_element(By.NAME, "USER_PASSWORD").send_keys("test123test123")

# Нажатие на кнопку "Войти"
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Ожидание перехода на страницу личного кабинета
try:
    WebDriverWait(driver, 10).until(
        EC.url_to_be("https://www.stenova.ru/profile/")
    )
    print("Авторизация успешна!")
except TimeoutException:
    print("Ошибка авторизации!")

# Принять cookie
cookie_button = WebDriverWait(driver,10).until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[1]/div/button[1]"))
)
cookie_button.click()

# 2. Добавление обоев в корзину
# Находим кнопку "Обои"
catalog_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[@href='/catalog/']"))
)
catalog_button.click()
time.sleep(2)

# Переход в каталог обоев
driver.find_element(By.CSS_SELECTOR, ".catalog-card__container").click()
time.sleep(2)

# Проверка, что мы находимся в разделе обои
try:
    WebDriverWait(driver, 10).until(
        EC.url_to_be("https://www.stenova.ru/oboi/")
    )
    print("Мы в разделе обои!")
except TimeoutException:
    print("Ошибка: Мы не в разделе обои!")

# Выбор дизайна обоев
driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[2]/div[1]/div[1]/article/a").click()
time.sleep(2)

# Скролим до нужного элемента (обоев)
target_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-card__image"))
)
driver.execute_script("arguments[0].scrollIntoView();", target_element)
time.sleep(1)

# Наводим мышку на обои
product_card = driver.find_element(By.CSS_SELECTOR, ".product-card__image")
actions = ActionChains(driver)
actions.move_to_element(product_card).perform()

# Добавление в корзину
driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[1]/div[1]/div[1]/article/div[2]/button").click()
time.sleep(2)

# 3. Добавление ламината в корзину
driver.find_element(By.XPATH, "//*[@id='bx_3218110189_78468']").click()
time.sleep(2)  # Переход в раздел ламинат

# Проверка, что мы находимся в разделе ламинат
try:
    WebDriverWait(driver, 10).until(
        EC.url_to_be("https://www.stenova.ru/laminat/")
    )
    print("Мы в разделе ламинат!")
except TimeoutException:
    print("Ошибка: Мы не в разделе ламинат!")

# Добавление в корзину
driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div/div/div[3]/div/div/article[1]/div[2]/button").click()
time.sleep(2)

# 4. Проверка корзины
driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div/div/div[3]/div/div/article[1]/div[2]/button").click()
time.sleep(2)

# Проверка, что мы находимся в корзине
try:
    WebDriverWait(driver, 10).until(
        EC.url_to_be("https://www.stenova.ru/cart/")
    )
    print("Мы в корзине!")
except TimeoutException:
    print("Ошибка: Мы не в корзине!")

# Проверка количества обоев
try:
    value1 = driver.find_element(By.XPATH, "//div[1]/div[2]/div/div/input")
    assert value1.get_attribute("value") == "1"
    print("Проверка количества обоев прошла успешно!")
except (NoSuchElementException, AssertionError):
    print("Ошибка: Количество обоев неверно!")

# Проверка количества ламината
try:
    value2 = driver.find_element(By.XPATH, "//div[2]/div[2]/div/div[2]/div/div/input")
    assert value2.get_attribute("value") == "1"
    print("Проверка количества ламината прошла успешно!")
except (NoSuchElementException, AssertionError):
    print("Ошибка: Количество ламината неверно!")


# Нажатие на кнопку "Оформить заказ"
driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[1]/aside/div/div[5]/a").click()
time.sleep(2)

# Проверка, что мы на странице оформления заказа
try:
    WebDriverWait(driver, 10).until(
        EC.url_to_be("https://www.stenova.ru/order/")
    )
    print("Мы на странице оформления заказа!")
except TimeoutException:
    print("Ошибка: Мы не на странице оформления заказа!")

# Удаление товаров из корзины для более удобного повторения автотеста
driver.get("https://www.stenova.ru/cart/")
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div[3]/main/div/div[1]/section/div[2]/div[1]/div/div[1]/div/button").click()
time.sleep(1)
driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div/div/button[1]").click()
time.sleep(1)

# Закрываем браузер
driver.quit()