var $box_each = $(".div-main button");

$box_each.click(function() {
  if ($(this).hasClass("clicked")) {
    $(this).addClass("unclicked");
    $(this).removeClass("clicked");
  } else {
    $(this).removeClass("unclicked");
    $(this).addClass("clicked");
    $box_each.css("opacity", "0.2");
    $(this).css("opacity", "1");
  }
});