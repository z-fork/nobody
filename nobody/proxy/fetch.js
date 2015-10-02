var page = require('webpage').create();

page.open(phantom.args[0], function(status) {
    if (status !== 'success') {
        console.log('Unable to access network');
    } else {
        var p = page.evaluate(function () {
            return document.getElementsByTagName("html")[0].innerHTML;
        });
        console.log(p);
    }
    phantom.exit();
});
