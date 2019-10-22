
//𝑆𝑐𝑜𝑟𝑒(𝐶𝑄, 𝑞′) = 𝐹𝑟𝑒𝑞(𝐶𝑄) + 𝑀𝑜𝑑(𝐶𝑄, 𝑞′) + 𝑇𝑖𝑚𝑒(𝐶𝑄, 𝑞′) / 1 − 𝑀𝑖𝑛{𝐹𝑟𝑒𝑞(𝐶𝑄), 𝑀𝑜𝑑(𝐶𝑄, 𝑞′), 𝑇𝑖𝑚𝑒(𝐶𝑄, 𝑞′)}
//where q’ is the n-gram triggering the suggestions, 𝐹𝑟𝑒𝑞(𝐶𝑄) is the frequency of occurrence of 𝐶𝑄 in QL
//divided by the maximum frequency of occurrence of any query in QL, 𝑀𝑜𝑑(𝐶𝑄, 𝑞′) is the number of
//sessions in which q’ is modified to 𝐶𝑄 divided by the total number of sessions in QL in which q’ appears,
//and 𝑇𝑖𝑚𝑒(𝐶𝑄, 𝑞′) is min difference between the time occurrence of q’ and 𝐶𝑄 across sessions in which
//both q’ and 𝐶𝑄 appear over length of the longest session in QL.
//https://select2.org/

function Get(yourUrl){
var Httpreq = new XMLHttpRequest(); // a new request
Httpreq.open("GET",yourUrl,false);
Httpreq.send(null);
return Httpreq.responseText;
}

function searchjs(term) {
  // var tData = JSON.parse(Get('https://api.myjson.com/bins/13p5yz'));
  // var tData = JSON.parse(Get('https://irnotinfrared.s3-us-west-2.amazonaws.com/aqlog.json'));

  // var tData = JSON.parse(queryLog);
  // var suggestions = [];
  // for (var i = 0; i < tData.length; i++){
  //     if (tData[i].query.includes(term))
  //         suggestions.push(tData[i].query);
  //         console.log(suggestions);
  //   }
    console.log(term)
    var t = term;
    $.ajax({
        type: "GET",
        url: "/search/",
        datatype: "text",
        async: false,
        data: {param : t},
        success: callbackFunc
    }).done(function (o) {
        // do something
    });
    /*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
    // autocomplete(document.getElementById("myInput"), suggestions);
}

// function postData(input) {
//     $.ajax({
//         type: "POST",
//         url: "/reverse_pca.py",
//         data: { param: input },
//         success: callbackFunc
//     });
// }

function callbackFunc(response) {
    /*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
    // console.log(response);
    // var tData = JSON.parse(response);
    var suggestions = [];
    // console.log(response.length);
    // for (var k in response){
    //     suggestions.push(k);
    // }
    var keys = Object.keys(response);
    var len = keys.length;
    keys.sort().reverse();
    var retvals = [];
    for (var i = 0; i < len; i++) {
        var k = keys[i];
        console.log(k + ':' + response[k]);
        suggestions.push(response[k]);
    }
    // //   if (tData[i].query.includes(term))
    //       suggestions.push(response[i]);
    //       console.log(k);
    // }
    // console.log(suggestions);
    autocomplete(document.getElementById("myInput"), suggestions);
}

function loadJSON(callback) {
  var xobj = new XMLHttpRequest();
  xobj.overrideMimeType("application/json");
  xobj.open('GET', '../../queryLog.json', true);
  xobj.onreadystatechange = function () {
    if (xobj.readyState == 4 && xobj.status == "200") {
      callback(JSON.parse(xobj.responseText));
    }
  };
  xobj.send(null);
}

function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

/*An array containing all the country names in the world:*/
// var countries =

// var tData = JSON.parse(queryLog);

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
// autocomplete(document.getElementById("myInput"), countries);
