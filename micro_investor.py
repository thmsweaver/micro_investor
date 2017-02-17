from collections import OrderedDict
import datetime
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains

from utils import script_readers

FIDELTY_BASE_URL = 'https://www.fidelity.com/'

ROTH_IRA_ACCOUNT_NUMBER = \
    os.environ.get('FIDELITY_ROTH_IRA_ACCOUNT_NUMBER')

ROTH_IRA_URL = (
    'https://oltx.fidelity.com/ftgw/fbc/oftop/portfolio'
    '#positions/{roth_ira_account_number}'
    .format(roth_ira_account_number=ROTH_IRA_ACCOUNT_NUMBER)
)

CONTRIBUTION_DEADLINE_MONTH = 4
CONTRIBUTION_DEADLINE_DAY = 16


def _wait_for_element_by_id(element_id, driver, duration=10):
    wait_params = (By.ID, element_id)
    found_element = WebDriverWait(driver, duration).until(
        ec.presence_of_element_located(wait_params)
    )
    return found_element


def _get_action_impl(element_id, element_to_action_map, actions):
    action_map = element_to_action_map[element_id]

    action_impl = getattr(actions, action_map['action'])
    if not action_impl:
        raise ValueError(
            'Element by id: {id} has no attribute: {attr}.'
            .format(id=element_id, attr=action_map['action'])
        )
    return action_map, action_impl


def get_days_remaining_to_contribute():
    now = datetime.datetime.now()
    deadline_this_year = datetime.datetime(
        now.year, CONTRIBUTION_DEADLINE_MONTH, CONTRIBUTION_DEADLINE_DAY
    )

    if now <= deadline_this_year:
        days = (deadline_this_year - now).days
    else:
        next_year = now.year + 1
        deadline_of_next_year = datetime.datetime(
            next_year, CONTRIBUTION_DEADLINE_MONTH, CONTRIBUTION_DEADLINE_DAY
        )
        days = (deadline_of_next_year - now).days

    # we'd still like to contribute on the day of the deadline
    return days + 1


def _login(element_to_action_map, driver):

    for e_id in element_to_action_map.keys():
        actions = ActionChains(driver)

        found_element = _wait_for_element_by_id(e_id, driver)
        actions.click(found_element)

        action_map, action_impl = _get_action_impl(
            e_id, element_to_action_map, actions)

        if action_map.get('param'):
            action_impl(action_map['param'])
        else:
            action_impl()

        actions.perform()
        # allow JS engine to 'tick',
        # input focus lag is prone to 'stealing' characters.
        time.sleep(0.5)


def login(driver):
    driver.get(FIDELTY_BASE_URL)

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
    _login(element_to_action_map, driver)


def go_to_roth_ira_account(driver):
    login(driver)

    # TODO: js tick?
    time.sleep(1)

    driver.get(ROTH_IRA_URL)

    # TODO: js tick?
    time.sleep(1)


def _wait_for_js_tables(driver):
    def are_js_tables_loaded(driver):
        tabels_length = driver.execute_script(
            "return $('.p-positions-tbody').length"
        )
        return int(tabels_length) > 1

    WebDriverWait(driver, 10).until(are_js_tables_loaded)


def _get_core_position_cash(driver):
    core_position_cash = driver.execute_script(
        script_readers.get_core_position_cash()
    )
    return float(re.sub('[^\d\.]', '', core_position_cash))


def _get_contribution_recommendation(driver):
    core_position_cash = _get_core_position_cash(driver)
    days_remaining_to_contribute = get_days_remaining_to_contribute()

    return core_position_cash / days_remaining_to_contribute


def alert_contribution_recommendation(driver):
    contribution_recommendation = _get_contribution_recommendation(driver)

    alert_script = (
        'alert("Young Thomas, contribute $' +
        str(contribution_recommendation) +
        ' today.")'
    )
    driver.execute_script(alert_script)


def go_to_contribution_advice(driver):
    go_to_roth_ira_account(driver)
    _wait_for_js_tables(driver)

    driver.execute_script(script_readers.open_fund_drawers())
    alert_contribution_recommendation(driver)


driver = webdriver.Chrome()
go_to_contribution_advice(driver)
