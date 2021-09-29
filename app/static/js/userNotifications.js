$(document).ready(function () {
    console.log(sessionStorage.getItem("visited"));
    $('#welcomeAlert').hide(); // can this be set by default i.e. with css? does jquery's "show()" simply change the css?
    $('.notification-toasts').hide();

    if (localStorage.getItem("wasVisited") == null) {
        $('#welcomeAlert').show();
        localStorage.setItem('wasVisited', 'true');
    };

    if (sessionStorage.getItem("visited") == null) {
        $('.toast').toast('show');
        $('.notification-toasts').show();
        sessionStorage.setItem('visited', 'true');
    };
});