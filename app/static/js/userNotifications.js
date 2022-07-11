$('#welcomeAlert').hide();
$('.notification-toasts').hide();

$(document).ready(function () {

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
