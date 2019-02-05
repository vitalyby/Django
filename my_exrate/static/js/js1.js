// console.log('Hello word')
//
// function f_sum(a, b) {
//     return a + b
// }
//
// console.log(f_sum(4, 5))
//
// function f_1(a) {
//     return a * 4
// }
//
// console.log(f_1(5))
//
// var username = $('#username').val();
//
// function showMessage() {
//     var message = 'Привет, я ' + username;
//     alert(message);
// }

// showMessage();

// function someFunc() {
//     alert(navigator.userAgent);
// }

// console.log(someFunc())

$(document).ready(function () {

    $('#but_am').click(function (e) {
        alert("Нажата кнопка id='but_am'")
    })

    $('#but_mat').click(function (e) {
        alert("Нажата кнопка id='but_mat'")
    })
    //обработка кнопки регистрации
    $('#register').click(function (e) {
        e.preventDefault()
        alert("register username='" + $('#username3').val() + "'")
        $.post("user_check", {'username': $('#username3').val()}, function (response) {
                alert("register0 username=" + response.user)
                if (response.user == 'user_exists') {
                    alert("Такое имя " + $('#username3').val() + " уже занято.")
                }
                else if (response.user == 'user_not_check') {
                    alert("Выберите другое username.")
                }
                else {
                    $.post("user_register", {
                            'username': $('#username3').val(),
                            'email': $('#email3').val(),
                            'password': $('#password3').val()
                        }, function (response) {
                            alert("register_end OK")
                            document.location.href = "/";
                        }
                    );
                }
            }
        );
    })
    $('#login').click(function (e) {
        if ($('#username').val() == '') {
            alert("login empty")
            e.preventDefault()
        }
        else {
            if ($('#password').val().length < 3) {
                alert("password short or empty")
                e.preventDefault()
            }
        }
    })
    $('#login2').click(function (e) {
        if ($('#username2').val() == 'admin') {
            alert("login2 : Hi admin")
            // e.preventDefault()
        }
        else {
            alert("login2 username='" + $('#username2').val() + "'")
        }
    })

});