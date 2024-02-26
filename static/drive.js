function filter_sites() {
  var text = document.getElementById("search_box").value;
  var list = document.getElementById("drive_sites");
  var items = list.getElementsByTagName("li");
  for (var i = 0; i < items.length; ++i) {
    var item = items[i];
    var item_text = item.textContent || item.innerText;
    item_text = item_text.toLowerCase();
    if (item_text.indexOf(text.toLowerCase()) > -1) {
      item.style.display = "block";
    } else {
      if (item_text != "extern") {
        item.style.display = "none";
      }
    }
  }
}
