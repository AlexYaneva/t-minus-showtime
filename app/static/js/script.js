

$(document).ready(function () {
    var currentPage = 2;
    var container = $('#scroller');
    var pathName = window.location.pathname;


    const observer = new IntersectionObserver(entries => {
        const firstEntry = entries[0];
        if (firstEntry.isIntersecting) {
            $.ajax($SCRIPT_ROOT + pathName + '?page=' + currentPage).done(function (data) {
                currentPage++;
                // data returned from the server is an html template
                container.append(data);
            })
        }
    });


    const sentinel = document.querySelector("#sentinel");
    observer.observe(sentinel);
});

