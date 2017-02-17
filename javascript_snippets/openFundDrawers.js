var FUND_SYMBOLS = [
    'FDEEX',
    'FPEMX',
    'FUSEX',
];
var $fundDrawers = $('.stock-symbol');

// first position is CORE, which we don't care to click on
for (var i = 1; i < $fundDrawers.length; i++) {
    var fundSymbol = $fundDrawers[i].innerText;
    if (~FUND_SYMBOLS.indexOf(fundSymbol)) $fundDrawers[i].click();
}
