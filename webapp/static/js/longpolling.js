function load_data() {
    let xhr = new XMLHttpRequest();
    xhr.open('GET', '/milewsp1/app/polling_data', false);
    xhr.onload = function () {
        if (this.responseText.length > 0) {
            console.log("aaaafddfaa");
            alert(this.responseText);
        }
    };
    xhr.send()
}

function long_polling() {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/milewsp1/app/long_polling_notify', true);
    xhr.onload = function () {
        if (this.responseText == "newFile") {
            load_data();
        }
        setTimeout(long_polling, 1500)
    };
    xhr.send();
}

long_polling();