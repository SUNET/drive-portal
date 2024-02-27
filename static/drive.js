function filter_sites() {
  var text = document.getElementById("search_box").value;
  var list = document.getElementById("drive_sites");
  var items = list.getElementsByTagName("li");
  var visible = false;
  var extern_id = 0;
  for (var i = 0; i < items.length; ++i) {
    var item = items[i];
    var item_text = item.textContent || item.innerText;
    item_text = item_text.toLowerCase();
    if (item_text.indexOf(text.toLowerCase()) > -1) {
      item.style.display = "block";
      visible = true;
    } else {
      item.style.display = "none";
    }
    if (item_text.indexOf('extern') > -1) {
      extern_id = i;
    }
  }
  if (!visible) {
    document.getElementById(extern_id).style.display = "block";
  }
}
