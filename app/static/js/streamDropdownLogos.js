$(document).ready(function () {

    var logoPath = "http://image.tmdb.org/t/p/original";
    var itemId = $("#content").attr("data");
    var pathName = "/watch_providers/";

    $.ajax($SCRIPT_ROOT + pathName + itemId).done(function (data) {
        var countries = data;
        changeStreamLogos(countries);
    });

    function changeStreamLogos(countries) {
        $("select")
            .change(function () {
                var countryCode = $("select").val();
                // $("#content").text(countryCode);
                try {
                    var watchFree = countries.results[countryCode].flatrate;
                }
                catch (err) {
                    try {
                        var watchFree = countries.results[countryCode].free;
                    }
                    catch (err) {
                        var watchFree = null;
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