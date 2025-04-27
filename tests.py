import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import allure

BASE_URL = "https://www.sibdar-spb.ru"
ID_COOKIE = "736599"
# --- API TESTS --- #


@allure.feature("API")
@allure.story("Add item to cart")
def test_add_item_to_cart():
    payload = {
        "idCookie": ID_COOKIE,
        "idProd": "178",
        "type": "add"
    }
    response = requests.post(f"{BASE_URL}/ajax/basketOrder.php", json=payload)
    assert response.status_code == 200
    assert response.json().get("success") is True


@allure.feature("API")
@allure.story("Update item quantity")
def test_update_cart_item():
    payload = {
        "idCookie": ID_COOKIE,
        "idProd": 178,
        "type": "plus"
    }
    response = requests.post(f"{BASE_URL}/ajax/basketOrder.php", json=payload)
    assert response.status_code == 200
    assert response.json()["item"]["quantity"] == 3


@allure.feature("API")
@allure.story("Remove item from cart")
def test_remove_item_from_cart():
    payload = {
        "idCookie": ID_COOKIE,
        "idProd": 178,
        "type": "delete"
    }
    response = requests.post(f"{BASE_URL}/ajax/basketOrder.php")
    assert response.status_code in [200, 204]


# --- UI TESTS --- #

@allure.feature("UI")
@allure.story("Add product to cart")
def test_ui_add_product_to_cart():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(BASE_URL)

    with allure.step("Открыть страницу товара"):
        driver.find_element(By.CSS_SELECTOR, ".product-card a").click()

    with allure.step("Добавить в корзину"):
        driver.find_element(By.CSS_SELECTOR, ".add-to-cart").click()

    with allure.step("Перейти в корзину и проверить товар"):
        driver.get(f"{BASE_URL}/cart")
        assert driver.find_element(By.CSS_SELECTOR, ".cart-item")

    driver.quit()


@allure.feature("UI")
@allure.story("Change quantity in cart")
def test_ui_change_quantity():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"{BASE_URL}/cart")

    with allure.step("Изменить количество"):
        quantity_input = driver.find_element(By.CSS_SELECTOR, ".cart-item-quantity")
        quantity_input.clear()
        quantity_input.send_keys("2")
        driver.find_element(By.CSS_SELECTOR, ".update-cart").click()

    with allure.step("Проверить обновление"):
        updated_quantity = driver.find_element(By.CSS_SELECTOR, ".cart-item-quantity").get_attribute("value")
        assert updated_quantity == "2"

    driver.quit()


@allure.feature("UI")
@allure.story("Remove item from cart")
def test_ui_remove_item():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"{BASE_URL}/cart")

    with allure.step("Удалить товар"):
        driver.find_element(By.CSS_SELECTOR, ".remove-item").click()

    with allure.step("Проверить, что корзина пуста"):
        assert "Корзина пуста" in driver.page_source

    driver.quit()