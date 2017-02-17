def _return_script(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        return data


def get_core_position_cash():
    return _return_script('javascript_snippets/getCorePositionCash.js')


def open_fund_drawers():
    return _return_script('javascript_snippets/openFundDrawers.js')
