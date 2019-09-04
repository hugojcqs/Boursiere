var db = {};
var current_quarter = 0;
var first_run = true;
$(document).ready(function() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
});



function calculate_price() {
    $.post({
        url: '/calculate_price/',
        data: {
            'data': JSON.stringify(db)
        },
        async: true,
        dataType: 'json',
        success: function(data) {
            let elem = $("#total_price");
            elem.text('Prix : ' + String(data['price']) + " €");
            check_order_stock(data['now_stock']);

        },
        error: function(xhr, status, error) {
            //TODO : handle error in ajax request
            console.log('Cannot update the stock page', status, error);
        }
    });
}


function connect() {

    let username = $("#usernamelogin")
    let password = $('#passwordlogin')

    console.log(username.val())
    console.log(password.val())

    console.log('Connection?');

}
