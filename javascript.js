function getIt() {
    return document.querySelectorAll('span[title="FIDELITY 500 INDEX INVESTOR CLASS"]');
}

result = getIt();
while (!result.length) {
    result = getIt();
}

result[0].click();
