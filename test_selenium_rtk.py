import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from settings import *
import time


# Типы авторизации
login_ways = [phone_number, email, login, account, phone_number, email]
# Идентификаторы вкладок при стандартной авторизации/восстановлении пароля
default_tab_ids = ['t-btn-tab-phone', 't-btn-tab-mail', 't-btn-tab-login', 't-btn-tab-ls']


@pytest.fixture(autouse=True)
def prepare_to_test():
    pytest.driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    pytest.driver.implicitly_wait(20)  # Неявное ожидание

    yield

    pytest.driver.quit()


def standart_authorization_tab_control(auth_type, pass_to_send):
    # Переходим на вкладку соответствующего типа
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.ID, default_tab_ids[auth_type]))
    )
    element.click()
    # Вводим cоответствующий логин
    pytest.driver.find_element(By.ID, 'username').send_keys(login_ways[auth_type])
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'password').send_keys(pass_to_send)
    # Нажимаем на кнопку входа в аккаунт
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    element.click()


def additional_authorization_with_sending_code_control(auth_type):
    if auth_type in [BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL]:
        # Вводим телефон или email
        pytest.driver.find_element(By.ID, 'address').send_keys(login_ways[auth_type])
        # Нажимаем на кнопку получения кода
        element = WebDriverWait(pytest.driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        element.click()
    else:  # Стандартная авторизация
        # Для каждого типа авторизации выбираем, какой пароль будем использовать (перебираем кейсы)
        pass_ways = [password, password, incorrect_password]
        # Нажимаем на кнопку для перехода на форму стандартной авторизации
        element = WebDriverWait(pytest.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'standard_auth_btn'))
        )
        element.click()
        # Первая загрузка, после нажатия кнопки мы можем остаться на текущей странице и получить неверный заголовок
        # Явные и неявные ожидания из WebDriver здесь не помогут
        timeout = 60  # Секунд
        timeout_end = time.time() + timeout
        # Простая проверка на наличие элемента на странице
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
        )
        # Если еще не перешли на другую страницу, начинаем опрашивать в цикле
        while (element.text == "Авторизация по коду" and time.time() < timeout_end):
            element = WebDriverWait(pytest.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
            )
        # Авторизуемся стандартным способом (если он доступен)
        standart_authorization_tab_control(auth_type, pass_ways[auth_type])


# Авторизация ЕЛК Web
def authorization_elk_web(auth_type):
    # Поддерживаемые типы аутентификации в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_ACCOUNT]:
        return
    # Для каждого типа авторизации выбираем, какой пароль будем использовать (перебираем кейсы)
    pass_ways = [password, password, incorrect_password, password]
    # Переходим на страницу авторизации
    pytest.driver.get(elk_web)
    # Авторизуемся стандартным способом (если он доступен)
    standart_authorization_tab_control(auth_type, pass_ways[auth_type])


# Авторизация Онлайм Web
def authorization_onlime_web(auth_type):
    # Поддерживаемые типы авторизации в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(online_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_authorization_with_sending_code_control(auth_type)


# Авторизация Старт Web
def authorization_start_web(auth_type):
    # Поддерживаемые типы авторизации в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_ACCOUNT, BY_CODE_TO_PHONE,
                         BY_CODE_TO_EMAIL]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(start_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_authorization_with_sending_code_control(auth_type)


# Авторизация Умный дом Web
def authorization_smart_home_web(auth_type):
    # Поддерживаемые типы авторизации в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_CODE_TO_PHONE,
                         BY_CODE_TO_EMAIL]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(smart_home_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_authorization_with_sending_code_control(auth_type)


# Авторизация Ключ Web
def authorization_key_web(auth_type):
    # Поддерживаемые типы авторизации в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_ACCOUNT, BY_CODE_TO_PHONE,
                         BY_CODE_TO_EMAIL]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(key_web)
    # Нажимаем на кнопку Войти
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="go_kab"]'))
    )
    element.click()
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_authorization_with_sending_code_control(auth_type)


def standart_recovery_tab_control(auth_type):
    # Нажимаем на кнопку Забыл пароль
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.ID, 'forgot_password'))
    )
    element.click()
    # Переходим на вкладку соответствующего типа
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.ID, default_tab_ids[auth_type]))
    )
    element.click()
    # Вводим cоответствующий логин
    pytest.driver.find_element(By.ID, 'username').send_keys(login_ways[auth_type])
    # Нажимаем на кнопку Продолжить
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[id="reset"]'))
    )
    element.click()


def additional_recovery_with_sending_code_control(auth_type):
    if auth_type in [BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL]:
        return
    else:  # Стандартное восстановление
        # Нажимаем на кнопку для перехода на форму стандартной авторизации
        element = WebDriverWait(pytest.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'standard_auth_btn'))
        )
        element.click()
        # Первая загрузка, после нажатия кнопки мы можем остаться на текущей странице и получить неверный заголовок
        # Явные и неявные ожидания из WebDriver здесь не помогут
        timeout = 60  # Секунд
        timeout_end = time.time() + timeout
        # Простая проверка на наличие элемента на странице
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
        )
        # Если еще не перешли на другую страницу, начинаем опрашивать в цикле
        while (element.text == "Авторизация по коду" and time.time() < timeout_end):
            element = WebDriverWait(pytest.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
            )
        # Восстановим пароль стандартным способом (если он доступен)
        standart_recovery_tab_control(auth_type)


# Восстановление доступа ЕЛК Web
def recovery_elk_web(auth_type):
    # Поддерживаемые типы восстановления доступа в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_ACCOUNT]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(elk_web)
    # Восстановим пароль стандартным способом (если он доступен)
    standart_recovery_tab_control(auth_type)


# Восстановление доступа Онлайм Web
def recovery_onlime_web(auth_type):
    # Поддерживаемые типы восстановления доступа в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(online_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_recovery_with_sending_code_control(auth_type)


# Восстановление доступа Старт Web
def recovery_start_web(auth_type):
    # Поддерживаемые типы восстановления доступа в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_ACCOUNT]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(start_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_recovery_with_sending_code_control(auth_type)


# Восстановление доступа Умный дом Web
def recovery_smart_home_web(auth_type):
    # Поддерживаемые типы восстановления доступа в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(smart_home_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_recovery_with_sending_code_control(auth_type)


# Восстановление доступа Ключ Web
def recovery_key_web(auth_type):
    # Поддерживаемые типы восстановления доступа в продукте, выходим, если не соответствует
    if auth_type not in [BY_PHONE, BY_EMAIL, BY_LOGIN, BY_ACCOUNT]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(key_web)
    # Нажимаем на кнопку Войти
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="go_kab"]'))
    )
    element.click()
    # Работаем с расширенной авторизацией с возможностью отправки кода
    additional_recovery_with_sending_code_control(auth_type)


def standart_registration_tab_control(data_set):
    firstnames = ['Аааааааааааааааааааааааааааааа', 'аа', 'аа', 'zz']
    lastnames = ['Аа', 'аааааааааааааааааааааааааааааа', 'аа', '11']
    emails = ['1@z.z', 'русскаяпочта@почта.рус', '70000000000', '3@z.z']
    passwords = ['1q3#$ss_sS', 'qwerty123', '1q3#$ss_sS', '1q3#$ss_sS']
    confirm_passwords = ['1q3#$ss_sS', 'qwerty', '2q3#$ss_sS', '1q3#$ss_sS']

    if len(firstnames) <= data_set:
        return

    # Нажимаем на кнопку Забыл пароль
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.ID, 'kc-register'))
    )
    element.click()
    # Вводим данные регистрации
    pytest.driver.find_element(By.NAME, 'firstName').send_keys(firstnames[data_set])
    pytest.driver.find_element(By.NAME, 'lastName').send_keys(lastnames[data_set])
    pytest.driver.find_element(By.ID, 'address').send_keys(emails[data_set])
    pytest.driver.find_element(By.ID, 'password').send_keys(passwords[data_set])
    pytest.driver.find_element(By.ID, 'password-confirm').send_keys(confirm_passwords[data_set])
    # Нажимаем на кнопку Зарегистрироваться
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    element.click()


# Проверка сценария, когда при вводе незарегистрированной почты или телефона
# система создает новую
def additional_registration_with_sending_code_control(auth_type, data_set=0):
    login_ways = ['', '', '', '', '70000000000', '1@z.z']

    if auth_type in [BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL]:
        # Вводим телефон или email
        pytest.driver.find_element(By.ID, 'address').send_keys(login_ways[auth_type])
        # Нажимаем на кнопку получения кода
        element = WebDriverWait(pytest.driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        element.click()
    else:  # Стандартная регистрация
        # Нажимаем на кнопку для перехода на форму стандартной авторизации
        element = WebDriverWait(pytest.driver, 10).until(
            ec.element_to_be_clickable((By.ID, 'standard_auth_btn'))
        )
        element.click()
        # Первая загрузка, после нажатия кнопки мы можем остаться на текущей странице и получить неверный заголовок
        # Явные и неявные ожидания из WebDriver здесь не помогут
        timeout = 60  # Секунд
        timeout_end = time.time() + timeout
        # Простая проверка на наличие элемента на странице
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
        )
        # Если еще не перешли на другую страницу, начинаем опрашивать в цикле
        while (element.text == "Авторизация по коду" and time.time() < timeout_end):
            element = WebDriverWait(pytest.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
            )
        # Восстановим пароль стандартным способом (если он доступен)
        standart_registration_tab_control(data_set)



# Регистрация ЕЛК Web
def registration_elk_web(data_set):
    # Переходим на страницу авторизации
    pytest.driver.get(elk_web)
    # Зарегистрируемся стандартным способом (если он доступен)
    standart_registration_tab_control(data_set)


# Регистрация Онлайм Web
def registration_onlime_web(auth_type, data_set=0):
    # Поддерживаемые типы регистрации через авторизацию в продукте, выходим, если не соответствует
    if auth_type not in [BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL, BY_NOTHING]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(online_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    # BY_NOTHING - для работы с обычной регистрацией по data_set
    additional_registration_with_sending_code_control(auth_type, data_set)


# Регистрация Старт Web
def registration_start_web(auth_type, data_set=0):
    # Поддерживаемые типы регистрации через авторизацию в продукте, выходим, если не соответствует
    if auth_type not in [BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL, BY_NOTHING]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(start_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    # BY_NOTHING - для работы с обычной регистрацией по data_set
    additional_registration_with_sending_code_control(auth_type, data_set)


# Регистрация Умный дом Web
def registration_smart_home_web(auth_type, data_set=0):
    # Поддерживаемые типы регистрации через авторизацию в продукте, выходим, если не соответствует
    if auth_type not in [BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL, BY_NOTHING]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(smart_home_web)
    # Работаем с расширенной авторизацией с возможностью отправки кода
    # BY_NOTHING - для работы с обычной регистрацией по data_set
    additional_registration_with_sending_code_control(auth_type, data_set)


# Регистрация Ключ Web
def registration_key_web(auth_type, data_set=0):
    # Поддерживаемые типы восстановления доступа в продукте, выходим, если не соответствует
    if auth_type not in [BY_CODE_TO_PHONE, BY_CODE_TO_EMAIL, BY_NOTHING]:
        return

    # Переходим на страницу авторизации
    pytest.driver.get(key_web)
    # Нажимаем на кнопку Войти
    element = WebDriverWait(pytest.driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="go_kab"]'))
    )
    element.click()
    # Работаем с расширенной авторизацией с возможностью отправки кода
    # BY_NOTHING - для работы с обычной регистрацией по data_set
    additional_registration_with_sending_code_control(auth_type, data_set)


###################################################################################################
# ТЕСТЫ
###################################################################################################
# Проверка успешной авторизации по телефону
# Проверяем ЕЛК Web
def test_phone_authorization_elk_web():
    authorization_elk_web(BY_PHONE)
    # Проверяем, что мы оказались на странице переадресации после успешной авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[1]/div[2]/a[1]'
    ).text == "Личный кабинет"


# Тест добавлен сюда для того, чтобы несколько неуспешных тестов не шли друг за другом,
# а после следующей успешной авторизации произошел сброс числа неудачных попыток;
# Проверка неуспешной авторизации по логину
# Проверяем ЕЛК Web
def test_login_authorization_elk_web():
    authorization_elk_web(BY_LOGIN)
    # Проверяем, что мы получили ошибку авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или пароль"


# Проверка успешной авторизации по телефону
# Проверяем Онлайм Web
def test_phone_authorization_onlime_web():
    authorization_onlime_web(BY_PHONE)
    # Проверяем, что мы оказались на странице переадресации после успешной авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/a'
    ).text == "Перейти"


# Тест добавлен сюда для того, чтобы несколько неуспешных тестов не шли друг за другом,
# а после следующей успешной авторизации произошел сброс числа неудачных попыток;
# Проверка неуспешной авторизации по логину
# Проверяем Онлайм Web
def test_login_authorization_onlime_web():
    authorization_onlime_web(BY_LOGIN)
    # Проверяем, что мы получили ошибку авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или пароль"


# Проверка успешной авторизации по email
# Проверяем ЕЛК Web
def test_email_authorization_elk_web():
    authorization_elk_web(BY_EMAIL)
    # Проверяем, что мы оказались на странице переадресации после успешной авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="root"]/div[2]/div[1]/div[1]/div[2]/a[1]'
    ).text == "Личный кабинет"


# Тест добавлен сюда для того, чтобы несколько неуспешных тестов не шли друг за другом,
# а после следующей успешной авторизации произошел сброс числа неудачных попыток;
# Проверка неуспешной авторизации по лицевому счету
# Проверяем ЕЛК Web
def test_account_authorization_elk_web():
    authorization_elk_web(BY_ACCOUNT)
    # Проверяем, что мы получили ошибку авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или пароль"


# Проверка успешной авторизации по email
# Проверяем Онлайм Web
def test_email_authorization_onlime_web():
    authorization_onlime_web(BY_EMAIL)
    # Проверяем, что мы оказались на странице переадресации после успешной авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/a'
    ).text == "Перейти"


# Проверка успешной авторизации по коду на телефон
def test_code_phone_authorization():
    authorization_onlime_web(BY_CODE_TO_PHONE)
    # Проверяем, сработал ли таймер повторной отправки кода
    try:
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[2]'))
        )
        assert element.text.startswith('Отправка') == True
    except BaseException:
        # Первая загрузка, после нажатия кнопки мы можем остаться на текущей странице и получить неверный заголовок
        # Явные и неявные ожидания из WebDriver здесь не помогут
        timeout = 60  # Секунд
        timeout_end = time.time() + timeout
        # Простая проверка на наличие элемента на странице
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
        )
        # Если еще не перешли на другую страницу, начинаем опрашивать в цикле
        while (element.text == "Авторизация по коду" and time.time() < timeout_end):
            element = WebDriverWait(pytest.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
            )
        # Проверяем, что мы оказались на странице подтверждения кода
        assert element.text == "Код подтверждения отправлен"


# Проверка успешной авторизации по коду на email
def test_code_email_authorization():
    authorization_onlime_web(BY_CODE_TO_EMAIL)
    # Проверяем, сработал ли таймер повторной отправки кода
    try:
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[2]'))
        )
        assert element.text.startswith('Отправка') == True
    except BaseException:
        # Первая загрузка, после нажатия кнопки мы можем остаться на текущей странице и получить неверный заголовок
        # Явные и неявные ожидания из WebDriver здесь не помогут
        timeout = 60  # Секунд
        timeout_end = time.time() + timeout
        # Простая проверка на наличие элемента на странице
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
        )
        # Если еще не перешли на другую страницу, начинаем опрашивать в цикле
        while (element.text == "Авторизация по коду" and time.time() < timeout_end):
            element = WebDriverWait(pytest.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
            )
        # Проверяем, что мы оказались на странице подтверждения кода
        assert element.text == "Код подтверждения отправлен"


# Проверка успешной авторизации по телефону
# Проверяем Старт Web
def test_phone_authorization_start_web():
    authorization_start_web(BY_PHONE)
    # Проверяем, что мы оказались на странице переадресации после успешной авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="root"]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[3]'
    ).text == "Личный кабинет"


# Проверка успешной авторизации по телефону
# Проверяем Умный дом Web
def test_phone_authorization_smart_home_web():
    authorization_smart_home_web(BY_PHONE)
    # Проверяем, что мы оказались на странице переадресации после успешной авторизации
    assert pytest.driver.find_element(
        By.CSS_SELECTOR, 'span[class="openerLabel___2NCiG"]'
    ).text == "Мой умный дом"


# Проверка успешной авторизации по телефону
# Проверяем Ключ Web
def test_phone_authorization_key_web():
    authorization_key_web(BY_PHONE)
    # Проверяем, что мы оказались на странице переадресации после успешной авторизации
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="main"]/main[1]/div[1]/div[1]/a[1]/div[1]'
    ).text == "Ростелеком \nКлюч"


# Проверка неуспешного восстановления по телефону
# Проверяем ЕЛК Web
def test_phone_recovery_elk_web():
    recovery_elk_web(BY_PHONE)
    # Проверяем, что мы получили ошибку восстановления
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или текст с картинки"


# Проверка неуспешного восстановления по телефону
# Проверяем Онлайм Web
def test_phone_recovery_onlime_web():
    recovery_onlime_web(BY_PHONE)
    # Проверяем, что мы получили ошибку восстановления
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или текст с картинки"


# Проверка неуспешного восстановления по телефону
# Проверяем Старт Web
def test_phone_recovery_start_web():
    recovery_start_web(BY_PHONE)
    # Проверяем, что мы получили ошибку восстановления
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или текст с картинки"


# Проверка неуспешного восстановления по телефону
# Проверяем Умный дом Web
def test_phone_recovery_smart_home_web():
    recovery_smart_home_web(BY_PHONE)
    # Проверяем, что мы получили ошибку восстановления
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или текст с картинки"


# Проверка неуспешного восстановления по телефону
# Проверяем Ключ Web
def test_phone_recovery_key_web():
    recovery_key_web(BY_PHONE)
    # Проверяем, что мы получили ошибку восстановления
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/p'
    ).text == "Неверный логин или текст с картинки"


# Проверка успешной регистрации
# Проверяем ЕЛК Web
def test_registration_elk_web():
    registration_elk_web(0)
    # Проверяем, что мы оказались на странице с подтверждением email
    assert pytest.driver.find_element(
        By.XPATH, '//*[@id="page-right"]/div/div/h1'
    ).text == "Подтверждение email"


# Проверка неуспешной регистрации через авторизацию и получение кода по телефону
# Проверяем Онлайм Web
def test_by_code_to_phone_registration_onlime_web():
    registration_onlime_web(BY_CODE_TO_PHONE)
    # Проверяем, сработал ли таймер повторной отправки кода
    try:
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[2]'))
        )
        assert element.text.startswith('Отправка') == True
    except BaseException:
        # Первая загрузка, после нажатия кнопки мы можем остаться на текущей странице и получить неверный заголовок
        # Явные и неявные ожидания из WebDriver здесь не помогут
        timeout = 60  # Секунд
        timeout_end = time.time() + timeout
        # Простая проверка на наличие элемента на странице
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
        )
        # Если еще не перешли на другую страницу, начинаем опрашивать в цикле
        while (element.text == "Авторизация по коду" and time.time() < timeout_end):
            element = WebDriverWait(pytest.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
            )
        # Проверяем, что мы оказались на странице подтверждения кода
        assert element.text == "Код подтверждения отправлен"


# Проверка неуспешной регистрации через авторизацию и получение кода по email
# Проверяем Онлайм Web
def test_by_code_to_email_registration_onlime_web():
    registration_onlime_web(BY_CODE_TO_EMAIL)
    # Проверяем, сработал ли таймер повторной отправки кода
    try:
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.XPATH, '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[2]'))
        )
        assert element.text.startswith('Отправка') == True
    except BaseException:
        # Первая загрузка, после нажатия кнопки мы можем остаться на текущей странице и получить неверный заголовок
        # Явные и неявные ожидания из WebDriver здесь не помогут
        timeout = 60  # Секунд
        timeout_end = time.time() + timeout
        # Простая проверка на наличие элемента на странице
        element = WebDriverWait(pytest.driver, 10).until(
            ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
        )
        # Если еще не перешли на другую страницу, начинаем опрашивать в цикле
        while (element.text == "Авторизация по коду" and time.time() < timeout_end):
            element = WebDriverWait(pytest.driver, 10).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))
            )
        # Проверяем, что мы оказались на странице подтверждения кода
        assert element.text == "Код подтверждения отправлен"


# Проверка неуспешной регистрации, введенные данные не прошли проверки
# Проверяем Старт Web
def test_registration_start_web():
    registration_start_web(BY_NOTHING, 1)
    # Получаем ошибку валидации введенных данных при регистрации
    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[3]/span[1]'))
    )
    assert element.text.startswith("Введите") == True

    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[4]/div[1]/span[1]'))
    )
    assert element.text == "Пароль должен содержать хотя бы одну заглавную букву"

    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[4]/div[2]/span[1]'))
    )
    assert element.text == "Длина пароля должна быть не менее 8 символов"


# Проверка неуспешной регистрации, введенные данные не прошли проверки
# Проверяем Умный дом Web
def test_registration_smart_home_web():
    registration_smart_home_web(BY_NOTHING, 2)
    # Получаем ошибку валидации введенных данных при регистрации
    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[4]/div[2]/span[1]'))
    )
    assert element.text == "Пароли не совпадают"


# Проверка неуспешной регистрации, введенные данные не прошли проверки
# Проверяем Ключ Web
def test_registration_key_web():
    registration_key_web(BY_NOTHING, 3)
    # Получаем ошибку валидации введенных данных при регистрации
    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[1]/span[1]'))
    )
    assert element.text == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."

    element = WebDriverWait(pytest.driver, 10).until(
        ec.presence_of_element_located((By.XPATH,
                                        '//*[@id="page-right"]/div[1]/div[1]/div[1]/form[1]/div[1]/div[2]/span[1]'))
    )
    assert element.text == "Необходимо заполнить поле кириллицей. От 2 до 30 символов."