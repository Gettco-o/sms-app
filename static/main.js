var scrollpos = window.scrollY;
var header = document.getElementById("header");
var navcontent = document.getElementById("nav-content");
var navaction = document.getElementById("navAction");
var brandname = document.getElementById("brandname");
var toToggle = document.querySelectorAll(".toggleColour");

document.addEventListener("scroll", function () {
/*Apply classes for slide in bar*/
scrollpos = window.scrollY;

if (scrollpos > 10) {
    header.classList.add("bg-white");
    navaction.classList.remove("bg-white");
    navaction.classList.add("gradient");
    navaction.classList.remove("text-gray-800");
    navaction.classList.add("text-white");
    //Use to switch toggleColour colours
    for (var i = 0; i < toToggle.length; i++) {
    toToggle[i].classList.add("text-gray-800");
    toToggle[i].classList.remove("text-white");
    }
    header.classList.add("shadow");
    navcontent.classList.remove("bg-gray-100");
    navcontent.classList.add("bg-white");
} else {
    header.classList.remove("bg-white");
    navaction.classList.remove("gradient");
    navaction.classList.add("bg-white");
    navaction.classList.remove("text-white");
    navaction.classList.add("text-gray-800");
    //Use to switch toggleColour colours
    for (var i = 0; i < toToggle.length; i++) {
    toToggle[i].classList.add("text-white");
    toToggle[i].classList.remove("text-gray-800");
    }

    header.classList.remove("shadow");
    navcontent.classList.remove("bg-white");
    navcontent.classList.add("bg-gray-100");
}
});

/*Toggle dropdown list*/
/*https://gist.github.com/slavapas/593e8e50cf4cc16ac972afcbad4f70c8*/

var navMenuDiv = document.getElementById("nav-content");
var navMenu = document.getElementById("nav-toggle");

document.onclick = check;
function check(e) {
var target = (e && e.target) || (event && event.srcElement);

//Nav Menu
if (!checkParent(target, navMenuDiv)) {
    // click NOT on the menu
    if (checkParent(target, navMenu)) {
    // click on the link
    if (navMenuDiv.classList.contains("hidden")) {
        navMenuDiv.classList.remove("hidden");
    } else {
        navMenuDiv.classList.add("hidden");
    }
    } else {
    // click both outside link and outside menu, hide menu
    navMenuDiv.classList.add("hidden");
    }
}
}
function checkParent(t, elm) {
while (t.parentNode) {
    if (t == elm) {
    return true;
    }
    t = t.parentNode;
}
return false;
}


// notification
const notificationBox = document.getElementById('notificationBox');
const notificationContent = document.getElementById('notificationContent');
const closeNotificationButton = document.getElementById('closeNotification');


closeNotificationButton.addEventListener('click', () => {
    notificationBox.classList.add('hidden');
  });

if (notificationBox) setTimeout(() => {
    notificationBox.classList.add('hidden');
}, 4000);


//receive sms

var country_id;
var application_id;

function toggleCountryDropdown() 
{
    const countryList = document.getElementById('countryList');
    countryList.classList.toggle('hidden');
}

function selectCountry(country, code, id) 
{
    const countryDropdown = document.getElementById('countryDropdown');
    countryDropdown.querySelector('span').innerHTML =` <img src=" ${'https://hatscripts.github.io/circle-flags/flags/' + code.toLowerCase() + '.svg'}" alt="${country}" class="inline-block w-5 h-5 mr-2"
    onerror="this.onerror=null;this.src='https://hatscripts.github.io/circle-flags/flags/ca.svg';">
    ${country}`;

    toggleCountryDropdown();
    country_id = id;
    console.log(country_id);

    getPrices();
}

// Close dropdown if clicked outside
document.addEventListener('click', function(event) 
{
    const countryDropdown = document.getElementById('countryDropdown');
    const countryList = document.getElementById('countryList');
    if (!countryDropdown.contains(event.target) && !countryList.contains(event.target)) {
      countryList.classList.add('hidden');
    }
});


function toggleServiceDropdown() 
{
    const serviceList = document.getElementById('serviceList');
    serviceList.classList.toggle('hidden');
}

function selectService(service, code, id) 
{
    const serviceDropdown = document.getElementById('serviceDropdown');
    serviceDropdown.querySelector('span').innerHTML =` <img src=" ${'https://imagedelivery.net/cg2aWO7l_BnFQQ6dZHYOSA/services/' + code.toLowerCase() + '.png/thumb'} " alt="${service}" class="inline-block w-5 h-5 mr-2"
    onerror="this.onerror=null;this.src='https://imagedelivery.net/cg2aWO7l_BnFQQ6dZHYOSA/services/wb.png/thumb';">
    ${service} `;

    toggleServiceDropdown();
    application_id = id;
    console.log(application_id);

    getPrices();
}

// Close dropdown if clicked outside
document.addEventListener('click', function(event) 
{
    const serviceDropdown = document.getElementById('serviceDropdown');
    const serviceList = document.getElementById('serviceList');
    if (!serviceDropdown.contains(event.target) && !serviceList.contains(event.target)) {
      serviceList.classList.add('hidden');
    }
});

// get prices

function getPrices()
{
    const numberAvailable = document.getElementById('number-available');
    const amount = document.getElementById('amount');
    console.log(country_id)
    console.log(application_id)

    if (country_id && application_id) {
        showSpinner();
        fetch(`/get-prices/${application_id}/${country_id}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(response => response.json())
          .then(data => {
            numberAvailable.innerText = data.data.count;
            amount.innerText = data.data.cost;
            console.log(data);
            hideSpinner();
          })
          .catch(error => {
            alert("Error: Couldn't fetch data", error);
            hideSpinner();
            // document.getElementById('error').className = ''; // uncomment if you want to show an error message
          });
    }
}

// spinner loader

function showSpinner() {
    document.getElementById('spinner').classList.remove('hidden');
    document.getElementById('availability').classList.add('hidden');
}

function hideSpinner() {
    document.getElementById('spinner').classList.add('hidden');
    document.getElementById('availability').classList.remove('hidden');
}


//search

function filterServices() {
    var input = document.getElementById('serviceSearch');
    var filter = input.value.toLowerCase();
    var ul = document.getElementById('serviceList');
    var li = ul.getElementsByClassName('service-item');

    for (var i = 0; i < li.length; i++) {
        var txtValue = li[i].textContent || li[i].innerText;
        if (txtValue.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}

function filterCountries() {
    var input = document.getElementById('countrySearch');
    var filter = input.value.toLowerCase();
    var ul = document.getElementById('countryList');
    var li = ul.getElementsByClassName('country-item');

    for (var i = 0; i < li.length; i++) {
        var txtValue = li[i].textContent || li[i].innerText;
        if (txtValue.toLowerCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}


// change password

function change_password() {
    var npassw = document.getElementById('newpassword');
    var cnpassw = document.getElementById('cnewpassword');

    console.log(npassw.value)
    console.log(cnpassw.value)
    

    if (npassw.value !== cnpassw.value) {
        btn = document.getElementById('changepassbtn');
        msg = document.getElementById('changepassalert');
        msg.classList.remove('hidden')
    }
    else {
        btn.disabled = false;
        msg.classList.add('hidden')
    }

}

// forgaot password

function hideModal() {
    var modal = document.getElementById('forgot-modal');
    modal.classList.add('hidden');
}

function displayModal() {
    var modal = document.getElementById('forgot-modal');
    modal.classList.remove('hidden');
}