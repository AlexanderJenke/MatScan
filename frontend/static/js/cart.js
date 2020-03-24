function update(data) {
    let action = data['action'];
    let values = data['values'];

    if (action == 'setInnerHTMLById') {
        document.getElementById(values['id']).innerHTML = values['content'];
    }

    if (action == 'alert') {
        document.getElementById('alert_box').innerHTML += values;
        if (data['timeout']) {
            setTimeout(function () {
                $("#alert_" + data['uuid']).alert('close');
            }, data['timeout']);
        }
    }

    if (action == 'fill_modal') {
        document.getElementById('dateModalContent').innerHTML = values;
    }

    if (action == 'show_modal') {
        $('#dateModal').modal('show');
    }

}

function trigger_event(args) {
    $.get("event", args);
}

function poll_started() {
    trigger_event({'action': 'get_cart'});
    setTimeout(trigger_event, 1000, {'action': 'get_cart'});
}