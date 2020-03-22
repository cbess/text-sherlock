/**
 * Provides clients side logic for the search pages
 */

var TSSearch = {
    // handles search page loading
    onPageLoad: function() {
        $('.result').click(function() {
            // show the corresponding document
            var url = $(this).find('.filename a').attr('href');
            location.href = url;
        });

        // focus the search field
        $("#text").focus();
    }
};

if (document.readyState === "complete" ||
    (document.readyState !== "loading" && !document.documentElement.doScroll)) {
  TSSearch.onPageLoad();
} else {
  document.addEventListener("DOMContentLoaded", TSSearch.onPageLoad);
}
