/**
 * Created by Ali.NET on 6/26/2020.
 */
var counter = 0;
var max_try = 20;
function bind_selector() {
    var dropdown = $("#id_country");
    if (!dropdown || dropdown.length == 0) {
        if (counter > max_try) return;
        setTimeout(bind_selector, 1000);
        return;
    }
    var city_dropdown = $("#id_city");

    dropdown.change(function () {
        var countryId = $(this).val();
        if (countryId) {
            $.ajax({
                url: url,
                data: {
                    'country': countryId
                },
                success: function (data) {
                    city_dropdown.html(data);
                }
            });
        } else {
            city_dropdown.html('<option value="" selected="">---------</option>');
        }
    });
}
bind_selector();
