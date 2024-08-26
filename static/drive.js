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

// Datalist field
let user_input = document.getElementById("site_input");

// Handling input event to avoid extra enter click when mouse selecting option for Firefox
user_input.addEventListener("input", (event) => {
  let event_type = event.inputType;
  if (event_type == "insertReplacementText") {
    optionChanged(event);

    //Shifts focus from input
    user_input.blur();
  }
});

// Fires on typing and key selecting
user_input.addEventListener("change", (event) => {
  // Type min 2 letters to avoid long button list
  if (event.target.value.length > 1) {
    optionChanged(event);

    //Shifts focus from input
    user_input.blur();
  }
});

// Shows options on first click for Firefox
user_input.addEventListener("mouseover", (event) => {
  user_input.focus();
});

// Clearing input when revisiting
user_input.addEventListener("focus", (event) => {
  user_input.value = "";
});

// Filtering site-button-list using datalist/input
function optionChanged(event) {
  var user_input_text = event.target.value.toLowerCase();
  var list = document.getElementById("drive_sites");
  var items = list.getElementsByTagName("li");

  var visible = false;
  var extern_id = 0;

  for (var i = 0; i < items.length; ++i) {
    let link = items[i].getElementsByTagName("a")[0];

    // Hide previous result
    items[i].style.display = "none";

    // Lower case site comparables
    var link_text = link.innerText.toLowerCase();
    var shortname = link.dataset.shortname.toLowerCase();
    var external_url = link.dataset.externalurl.toLowerCase();

    // Match input to site name, url or short name to match visible options
    var condition =
      link_text.includes(user_input_text) ||
      shortname.includes(user_input_text) ||
      external_url.includes(user_input_text);

    if (condition) {
      items[i].style.display = "block";
      visible = true;
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
