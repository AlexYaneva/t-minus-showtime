$(document).ready(function () {

    let logoPath = "http://image.tmdb.org/t/p/original";
    let itemId = $("#content").attr("data");
    let mediaType = $("#stream_dropdown").attr("data");
    let pathName = `/${mediaType}_watch/`;

    $.ajax($SCRIPT_ROOT + pathName + itemId).done(function (data) {
        let countries = data;
        changeStreamLogos(countries);
    });

    function changeStreamLogos(countries) {
        $("select")
            .change(function () {
                let countryCode = $("select").val();
                let watchFree;
                try {
                    watchFree = countries.results[countryCode].flatrate;
                }
                catch (err) {
                    try {
                        watchFree = countries.results[countryCode].free;
                    }
                    catch (err) {
                        watchFree = undefined;
                    }
                }
                if (watchFree !== undefined) {
                    $("#content").empty();
                    watchFree.forEach((item) => {
                        item.logo_path = logoPath + item.logo_path;
                        $("#content").append("<img class='logo' src='" + item.logo_path + "'>")


                    });
                }
                else {
                    $("#content").empty();
                    $("#content").append("<h6> Not available in this country </h6>");
                }

            });
    }
});