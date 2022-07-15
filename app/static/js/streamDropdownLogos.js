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
                // $("#content").text(countryCode);
                try {
                    let watchFree = countries.results[countryCode].flatrate;
                }
                catch (err) {
                    try {
                        let watchFree = countries.results[countryCode].free;
                    }
                    catch (err) {
                        let watchFree = null;
                    }
                }
                if (watchFree !== null) {
                    $("#content").empty();
                    watchFree.forEach((item) => {
                        item.logo_path = logoPath + item.logo_path;
                        $("#content").append("<img class='logo' src='" + item.logo_path + "'>")


                    });
                }
                else {
                    $("#content").empty();
                    $("#content").append("<h6> Not available </h6>");
                }

            });
    }
});