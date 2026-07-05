import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    #Address setup elements
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    # Taxi selection elements
    pick_a_taxi = (By.XPATH, '//div[@class="results-text"]//button[text()="Pedir un taxi"]')
    ride_comfort = (By.ID, 'tariff-card-4')
    tariff_comfort = (By.XPATH, '//div[@class="tcard active"]//div[@class="tcard-title"]')
    #Phone setup elements
    form_phone = (By.CSS_SELECTOR, '.np-button')
    phone_field = (By.ID, 'phone')
    popup_form_phone_add_button = (By.XPATH, '//div[@class="buttons"]//button[text()="Siguiente"]')
    phone_code_field = (By.ID, 'code')
    confirm_button = (By.XPATH, '//div[@class="buttons"]//button[text()="Confirmar"]')
    popup_form_phone_close_button = (By.XPATH, '//div[@class="section active"]//button[@class="close-button section-close"]')
    #Payment elements
    payment_field = (By.CSS_SELECTOR, '.pp-value')
    popup_add_card = (By.CSS_SELECTOR, '.pp-plus')
    card_number_field = (By.XPATH, '//input[@id="number"]')
    card_code_field = (By.XPATH, '//div[@class="card-code-input"]//input[@id="code"]')
    add_card_button = (By.XPATH, '//div[@class="pp-buttons"]//button[@class="button full"]')
    close_pay_list = (By.XPATH, '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    payment_method = (By.XPATH, '//div[@class="pp-button filled"]//div[@class="pp-value-text"]')
    #Add comment to driver elements
    comment_field = (By.ID, 'comment')
    error_in_comment = (By.XPATH, '//div[@class="input-container error"]')
    comment_error_type = (By.XPATH, '//div[@style="margin-top: 12px;"]//div[@class="error"]')
    #Requests header elements
    listing_request = (By.XPATH, '//div[@class="reqs-body"]')
    blanket_switch = (By.XPATH, '//div[@class="r-sw-container"][1]//input[@class="switch-input"]')
    switch_blanket_label = (By.CSS_SELECTOR, '.r-sw-label')
    icecream_select = (By.XPATH, '//div[contains(.,"Helado")]')
    add_icecream_tub = (By.CLASS_NAME, 'counter-plus')
    icecream_label = (By.XPATH, '//div[@class="r-group-items"][1]//div[@class="r-counter-label"]')
    icecream_tub_count = (By.XPATH, '//div[@class="r-group-items"][1]//div[@class="counter-value"]')
    #Get a taxi
    reserve_taxi_button = (By.CLASS_NAME, 'smart-button')
    order_countdown_timer = (By.CLASS_NAME, 'order-header-time')
    header_in_reserve_taxi_popup = (By.XPATH, '//div[@class="order-header-title"]')
    #Modal to retrieve a chauffeur
    car_chauffeur = (By.XPATH, '//div[@class="order-btn-group"]//div[2]')
    order_number = (By.XPATH, '//div[@class="order-number"]//div[@class="number"]')

    def __init__(self, driver):
        self.driver = driver
    #Address methods
    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')
    #Taxi selection methods
    def get_pick_taxi(self):
        self.driver.find_element(*self.pick_a_taxi).click()

    def get_ride_comfort(self):
        comfort_car=self.driver.find_element(*self.ride_comfort)
        self.driver.execute_script("arguments[0].click();",comfort_car)

    def check_comfort_title_card(self):
        return self.driver.find_element(*self.tariff_comfort).text
    #Phone field methods
    def get_phone_field(self):
        self.driver.find_element(*self.form_phone).click()

    def set_phone(self, phone_number):
        self.driver.find_element(*self.phone_field).send_keys(phone_number)

    def get_next_button_phone_form(self):
        self.driver.find_element(*self.popup_form_phone_add_button).click()

    def set_code_field(self,phone_code):
        self.driver.find_element(*self.phone_code_field).send_keys(phone_code)

    def get_confirm_phone_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def get_close_phone_form_button(self):
        close_form = self.driver.find_element(*self.popup_form_phone_close_button)
        self.driver.execute_script("arguments[0].click();", close_form)

    def check_phone_number_added(self):
        phone = self.driver.find_element(*self.phone_field).get_property('value')
        return phone
    #Payment methods
    def get_payment_field(self):
        change_pay_type = self.driver.find_element(*self.payment_field)
        self.driver.execute_script("arguments[0].click();", change_pay_type)

    def get_add_card_form(self):
        self.driver.find_element(*self.popup_add_card).click()

    def set_card_number(self, card_number):
        self.driver.find_element(*self.card_number_field).send_keys(card_number, Keys.TAB)

    def get_cvv_field_code(self):
        code_get_active = self.driver.find_element(*self.card_code_field)
        self.driver.execute_script("arguments[0].click();", code_get_active)

    def set_code_card(self, card_code):
        self.driver.find_element(*self.card_code_field).send_keys(card_code)

    def get_add_card_button(self):
        cc_code = self.driver.find_element(*self.card_code_field)
        self.driver.execute_script("arguments[0].blur();", cc_code)
        self.driver.find_element(*self.add_card_button).click()

    def get_close_payment_list_button(self):
        close_list = self.driver.find_element(*self.close_pay_list)
        self.driver.execute_script("arguments[0].click();", close_list)

    def get_payment_type(self):
        view_pay = self.driver.find_element(*self.payment_field)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", view_pay)
        return self.driver.find_element(*self.payment_method).get_attribute('innerHTML')
    #Add comment to driver method
    def select_comment_for_driver_field(self):
        view_comment_field = self.driver.find_element(*self.comment_field)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", view_comment_field)

    def set_comment_for_driver(self,user_message):
        self.driver.find_element(*self.comment_field).send_keys(user_message)

    def get_comment_for_driver(self):
        return self.driver.find_element(*self.comment_field).get_attribute('value')

    def check_error_in_comment_is_displayed(self):
        WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located(self.error_in_comment))

    def check_error_in_comment_for_driver(self):
        return self.driver.find_element(*self.comment_error_type).text
    #Request methods
    def view_requests(self):
        list_request = self.driver.find_element(*self.listing_request)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", list_request)

    def set_blanket_request(self):
        switch_toggle = self.driver.find_element(*self.blanket_switch)
        self.driver.execute_script("arguments[0].click();", switch_toggle)

    def check_blanket_switch(self):
        return self.driver.find_element(*self.blanket_switch).is_selected()

    def check_blanket_switch_label(self):
        return self.driver.find_element(*self.switch_blanket_label).get_attribute('innerHTML')

    def view_icecream_selection(self):
        icecream_header = self.driver.find_element(*self.icecream_select)
        self.driver.execute_script("arguments[0].scrollIntoView();",icecream_header)

    def set_double_icecream_tubs_request(self):
        icecream= self.driver.find_element(*self.add_icecream_tub)
        icecream.click()
        self.driver.execute_script("arguments[0].blur();", icecream)
        icecream.click()

    def get_icecream_label(self):
        return self.driver.find_element(*self.icecream_label).get_attribute('innerHTML')

    def get_icecream_tub_amount(self):
        return self.driver.find_element(*self.icecream_tub_count).get_attribute('innerHTML')
    #Taxi reserve open modal
    def set_taxi_travel(self):
        self.driver.find_element(*self.reserve_taxi_button).click()

    def get_order_time_visible(self):
        return self.driver.find_element(*self.order_countdown_timer).get_attribute('innerHTML')

    def check_taxi_reserve_popup_is_opened(self):
        return self.driver.find_element(*self.header_in_reserve_taxi_popup).get_attribute('innerHTML')
    #Retrieve driver name and car
    def get_driver_name(self):
        return self.driver.find_element(*self.car_chauffeur).text

    def get_order_number(self):
        WebDriverWait(self.driver, 35). until(expected_conditions.presence_of_element_located(self.order_number))

    def check_car_order_number(self):
        return self.driver.find_element(*self.order_number).text



class TestUrbanRoutes:

        driver = None

        @classmethod
        def setup_class(cls):
            # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
            from selenium.webdriver.chrome.options import Options
            chrome_options = Options()
            chrome_options.set_capability('goog:loggingPrefs' , {'performance': 'ALL'})
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.get(data.urban_routes_url)
            cls.driver.implicitly_wait(10)


        def test_1_set_route(self):
            routes_page = UrbanRoutesPage(self.driver)
            address_from = data.address_from
            address_to = data.address_to
            routes_page.set_from(address_from)
            routes_page.set_to(address_to)
            assert routes_page.get_from() == address_from, f'Prueba fallo: Dirección "Desde" no coincide con el enviado para la prueba'
            assert routes_page.get_to() == address_to, f'Prueba fallo: Dirección "Hasta" no coincide con el enviado para la prueba'

        def test_2_set_comfort_ride(self):
            routes_page = UrbanRoutesPage(self.driver)
            routes_page.get_pick_taxi()
            routes_page.get_ride_comfort()
            check_title = routes_page.check_comfort_title_card()
            assert 'Comfort' in check_title, f'Prueba fallo: Selección de tarifa diferente'

        def test_3_set_phone(self):
            routes_page = UrbanRoutesPage(self.driver)
            phone_user = data.phone_number
            routes_page.get_phone_field()
            routes_page.set_phone(phone_user)
            routes_page.get_next_button_phone_form()
            code = retrieve_phone_code(self.driver)
            routes_page.set_code_field(code)
            routes_page.get_confirm_phone_button()
            routes_page.get_close_phone_form_button()
            check_phone = routes_page.check_phone_number_added()
            assert check_phone == phone_user, f'Prueba fallo: Número de teléfono no coincide con el enviado para la prueba'

        def test_4_set_payment(self):
            routes_page = UrbanRoutesPage(self.driver)
            code_card = data.card_code
            number_card = data.card_number
            routes_page.get_payment_field()
            routes_page.get_add_card_form()
            routes_page.set_card_number(number_card)
            routes_page.get_cvv_field_code()
            routes_page.set_code_card(code_card)
            routes_page.get_add_card_button()
            routes_page.get_close_payment_list_button()
            card_pay = routes_page.get_payment_type()
            assert 'Tarjeta' in card_pay
            assert 'Efectivo' not in card_pay

        def test_5_error_in_set_comment(self):
            routes_page = UrbanRoutesPage(self.driver)
            comment_to_set = data.message_for_driver
            routes_page.select_comment_for_driver_field()
            routes_page.set_comment_for_driver(comment_to_set)
            get_new_comment =  routes_page.get_comment_for_driver()
            routes_page.check_error_in_comment_is_displayed()
            assert get_new_comment == comment_to_set, f'Prueba fallo: Mensaje introducido no coincide'
            assert routes_page.check_error_in_comment_for_driver(), f'Prueba fallo: Error al ingresar el comentario no se muestra'


        def test_6_set_request_for_blanket(self):
            routes_page = UrbanRoutesPage(self.driver)
            routes_page.view_requests()
            routes_page.set_blanket_request()
            blanket_label = routes_page.check_blanket_switch_label()
            assert 'Manta y pañuelos' == blanket_label, (f'Prueba fallo: Pedido no coincide con "Manta y pañuelos"')
            assert routes_page.check_blanket_switch()

        def test_7_set_request_for_icecream(self):
            routes_page = UrbanRoutesPage(self.driver)
            routes_page.view_icecream_selection()
            routes_page.set_double_icecream_tubs_request()
            icecream_label = routes_page.get_icecream_label()
            count_icecream_tub = routes_page.get_icecream_tub_amount()
            assert icecream_label == 'Helado', f'Prueba fallo: Pedido no coincide con "Helado"'
            assert count_icecream_tub == '2', f'Prueba fallo: Pedido de cantidad "2" helados no fue realizado'

        def test_8_open_request_taxi_window(self):
            routes_page = UrbanRoutesPage(self.driver)
            routes_page.set_taxi_travel()
            search_cab = routes_page.check_taxi_reserve_popup_is_opened()
            timer_countdown = routes_page.get_order_time_visible()
            assert any(word in search_cab.lower() for \
                       word in ['buscar', 'buscando']), f'Fallo: Ventana del modal de pedido de taxi no cargo de acuerdo a flujo de la aplicación'
            assert timer_countdown != "", f'Prueba fallo: Cuenta regresiva no aparece en la ventana del pedido de taxi'


        def test_9_driver_name_on_screen(self):
            routes_page = UrbanRoutesPage(self.driver)
            routes_page.get_order_number()
            order_number = routes_page.check_car_order_number()
            driver_new_name = routes_page.get_driver_name()
            print('Conductor: ', driver_new_name, 'Orden de viaje: ', order_number)
            assert routes_page.get_driver_name()
            assert driver_new_name != order_number
            assert routes_page.check_car_order_number()

        @classmethod
        def teardown_class(cls):
            cls.driver.quit()
