import os
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

FIDELTY_URL = 'https://www.fidelity.com/'
FUND_SYMBOLS = [
    'FDEEX',
    'FPEMX',
    'FUSEX',
]
ROTH_IRA_URL = (
    'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio'
    '#positions/{roth_ira_account_number}'
    .format(roth_ira_account_number=os.environ.get('ROTH_IRA_ACCOUNT_NUMBER'))
)

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
        browser.implicitly_wait(1)
        if action_map.get('param'):
            element_impl(action_map['param'])
        else:
            element_impl()

def login(browser):
    element_to_action_map = OrderedDict()
    element_to_action_map['userId-input'] = {
        'action': 'send_keys',
        'param': os.environ.get('FIDELTY_USERNAME')
    }
    element_to_action_map['password'] = {
        'action': 'send_keys',
        'param': os.environ.get('FIDELTY_PASSWORD')
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

import pdb; pdb.set_trace()

x = browser.find_element_by_xpath('//span[@title="FIDELITY 500 INDEX INVESTOR CLASS"]'
# first log out
# browser.quit()