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
                    console.log(err);
                    try {
                        var watchFree = countries.results[countryCode].free;
                    }
                    catch (err) {
                        console.log(err);
                        var watchFree = null;
                    }
                }
                console.log(watchFree);
                if (watchFree !== null) {
                    $("#content").empty();
                    watchFree.forEach((item) => {
                        item.logo_path = logoPath + item.logo_path;
                        $("#content").append("<img class='logo' src='" + item.logo_path + "'>")


                    });
                }

            });
    }
});