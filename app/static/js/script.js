var currentPage = 2;
var container = $('#scroller');
var pathName = window.location.pathname;


$(function () {
    $('#load_more').click(function () {
        $.ajax($SCRIPT_ROOT + pathName + '?page=' + currentPage).done(function (data) {
            currentPage++;
            // the returned data here contains structured html
            container.append(data);
        })
    })
});