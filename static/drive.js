function use_direct() {
  var list = document.getElementById("drive_sites");
  var items = list.getElementsByTagName("li");
  var checkbox_state = document.getElementById("direct_login").checked; 
  var suffix = "index.php/login?direct=1";
  for (var i = 0; i < items.length; ++i) {
    link = items[i].getElementsByTagName("a")[0];
    if (!checkbox_state) {
      if (link.href.indexOf( suffix ) != -1) {
        link.href = link.href.substring( 0, link.href.indexOf( suffix ) );
      }
    } else {
      link.href = link.href + suffix;
    }
  }

}
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
    if (item_text.indexof('extern') > -1) {
      extern_id = i;
    }
  }
  if (!visible) {
    document.getElementById(extern_id).style.display = "block";
  }
}
