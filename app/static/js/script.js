var currentPage = 2;
var container = $('#scroller');

$(function () {
    $('#load_more').click(function () {
        $.ajax($SCRIPT_ROOT + '/load_more' + '?page=' + currentPage).done(function (data) {
            currentPage++;
            // 'data' here contains structured html
            container.append(data);
        })
    })
});