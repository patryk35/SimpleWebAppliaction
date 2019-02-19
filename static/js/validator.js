function createValidationDiv(field_name, message, validationElemId) {
    let place = document.getElementById(field_name);
    let validation = document.createElement("div");
    validation.setAttribute("id", validationElemId);
    validation.setAttribute("class", "validation");
    let communicate = document.createTextNode(message);
    validation.appendChild(communicate);
    place.appendChild(validation);
}

function displayCommunicate(field_name, message) {
    let validationElemId = field_name + "_validation";
    let elem = document.getElementById(validationElemId)
    if (message != null && elem == null) {
        createValidationDiv(field_name, message, validationElemId)
    } else if (message == null && elem != null) {
        elem.parentNode.removeChild(elem);
    } else if (message != null && elem != null) {
        elem.parentNode.removeChild(elem);
        createValidationDiv(field_name, message, validationElemId)
    }
}

function validateField(field) {
    if (field.value.length == 0) {
        return "Pole musi byc wypelnione";
    }
    return null;
}

function initLoginForm() {
    let form = document.forms["loginForm"];
    let fields = ["login", "password"];
    for (let i = 0, len = fields.length; i < len; i++) {
        let field = form[fields[i]];
        field.addEventListener("blur", function () {
            let message = validateField(field);
            displayCommunicate(fields[i], message)
        });
    }
}

initLoginForm()