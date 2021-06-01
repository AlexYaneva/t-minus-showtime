
$(document).ready(function () {

    // reset the page counter every time a new tab is clicked
    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        currentPage = 2;
    })

    var currentPage = 2;

    // each time the user scrolls to the bottom of the page content, this function fires;
    // it grabs the active tab's id which is used to hit the corresponding server route;
    // it increments the page so that each time the observed div comes into view, the ajax request will get the next page of results
    // et voila the infinite scroll with tabs and that's all she wrote
    const observer = new IntersectionObserver(entries => {
        const firstEntry = entries[0];
        if (firstEntry.isIntersecting) {
            var activeTab = $(".tab-content").find(".active");
            var container = activeTab.find("#scroller");
            var pathName = activeTab.attr('id');
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






