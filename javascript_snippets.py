GET_CORE_POSITION_CASH = """
    var $positionsTable = $('.p-positions-tbody');
    var $corePositionRow = $($positionsTable.children()[1]);
    var corePositionCash = $corePositionRow.children()[4].innerText;
    return corePositionCash;
"""
