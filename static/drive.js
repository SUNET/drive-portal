// Direct login checkbox
function use_direct() {
  var list = document.getElementById("drive_sites");
  var items = list.getElementsByTagName("li");
  var checkbox_state = document.getElementById("direct_login").checked;
  var suffix = "index.php/login?direct=1";
  for (var i = 0; i < items.length; ++i) {
    link = items[i].getElementsByTagName("a")[0];
    if (!checkbox_state) {
      if (link.href.indexOf(suffix) != -1) {
        link.href = link.href.substring(0, link.href.indexOf(suffix));
      }
    } else {
      link.href = link.href + suffix;
    }
  }
}

// Filtering site-buttons using datalist/input
function optionChanged(event) {
  var text = document.getElementById("site").value;
  console.log(text);
  var list = document.getElementById("drive_sites");
  var items = list.getElementsByTagName("li");
  var visible = false;
  var extern_id = 0;
  for (var i = 0; i < items.length; ++i) {
    let link = items[i].getElementsByTagName("a")[0];
    var item_text = link.innerText;
    item_text = item_text.toLowerCase();
    var shortname = link.dataset.shortname;
    var condition =
      item_text.indexOf(text.toLowerCase()) > -1 ||
      shortname.indexOf(text.toLowerCase()) > -1;
    if (condition) {
      items[i].style.display = "block";
      visible = true;
    } else {
      items[i].style.display = "none";
    }
    if (shortname.indexOf("extern") > -1) {
      extern_id = i;
    }
  }
  if (!visible) {
    document.getElementById(extern_id).style.display = "inline";
  }
}

// Toggling info links in footer
function showMore() {
  document.getElementById("show_more").classList.toggle("shows");
  return false;
}
