(function poll() {
    var poll_interval = 0;

    $.ajax({
        url: "poll",
        type: 'GET',
        dataType: 'json',
        timeout: 31000,
        success: function (data, _, jqXHR) {
            if (jqXHR.status == 200) {
                update(data)
            }
            poll_interval = 0;
        },
        error: function () {
            poll_interval = 10000;
        },
        complete: function () {
            setTimeout(poll, poll_interval);
        },
    });
})();
poll_started();