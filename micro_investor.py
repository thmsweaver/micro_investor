import os
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

FIDELTY_URL = 'https://www.fidelity.com/'
FUND_SYMBOLS = [
    'FDEEX',
    'FPEMX',
    'FUSEX',
]
ROTH_IRA_URL = (
    'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio'
    '#positions/{roth_ira_account_number}'
    .format(roth_ira_account_number=os.environ.get('FIDELITY_ROTH_IRA_ACCOUNT_NUMBER'))
)


# TODO: use action chains here.
def _get_login_elements_and_send_action(element_to_action_map, browser):
    for element_id in element_to_action_map.keys():
        found_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        action_map = element_to_action_map[element_id]
        element_impl = getattr(found_element, action_map['action'])
        if not element_impl:
            raise ValueError(
                'Element by id: {id} has no attribute: {attr}.'
                .format(id=element_id, attr=action_map['action'])
            )

        # allow JS enginge to `tick` and avoid input focus lag,
        # which is prone to intercepting key-sent characters.
        # TODO: why does it happen and why won't this work?
        browser.implicitly_wait(5)
        if action_map.get('param'):
            element_impl(action_map['param'])
        else:
            element_impl()


def login(browser):
    element_to_action_map = OrderedDict()
    element_to_action_map['userId-input'] = {
        'action': 'send_keys',
        'param': os.environ.get('FIDELITY_USERNAME')
    }
    element_to_action_map['password'] = {
        'action': 'send_keys',
        'param': os.environ.get('FIDELITY_PASSWORD')
    }
    element_to_action_map['fs-login-button'] = {'action': 'click'}
    _get_login_elements_and_send_action(element_to_action_map, browser)


browser = webdriver.Chrome()
browser.get(FIDELTY_URL)
login(browser)

try:
    # waiting for element with `js` className indicates clickability
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'js-account'))
    )
except Exception as e:
    print e

# here the JS element could be clicked,
# but I harcoding the URL avoids DOM traversal
browser.get(ROTH_IRA_URL)
try:
    # waiting for element with `js` className indicates clickability
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'stock-symbol'))
    )
except Exception as e:
    print e


def _get_fusex():
    xpath = '//span[@title="FIDELITY 500 INDEX INVESTOR CLASS"]'
    try:
        fusex = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except Exception as e:
        print e
        _get_fusex

    try:
        fusex.click()
    except Exception as e:
        print e
        _get_fusex()

_get_fusex()

xpath = '//span[@title="FIDELITY 500 INDEX INVESTOR CLASS"]'
fusex = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, xpath))
)

with open('javascript.js', 'r') as file:
    data = file.read()

browser.execute_script(data)

# first log out
# browser.quit()
