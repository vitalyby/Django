console.log('Hello word')

function f_sum(a, b) {
    return a + b
}

console.log(f_sum(4, 5))

function f_1(a) {
    return a * 4
}

console.log(f_1(5))

var username = $('#username').val();

function showMessage() {
  var message = 'Привет, я ' + username;
  alert(message);
}

showMessage();

function someFunc(){
alert(navigator.userAgent);
}

console.log(someFunc())