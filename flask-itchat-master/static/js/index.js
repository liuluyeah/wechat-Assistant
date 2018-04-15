var autoCheck;

var Confirmed;
var xmlhttp = new XMLHttpRequest();
function login() {
	//var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("GET", "/php/login.php", true);
	xmlhttp.send();

	Confirmed = 0;
	autoCheck = setTimeout("checkLogin()", 2500);
}

function login2() {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("GET", "/php/login2.php", true);
	xmlhttp.send(null);
	Confirmed = 1;
	autoCheck = setTimeout("checkLogin()", 2500);
}


// function switchAccount() {
// 	clearTimeout(autoCheck);
// 	var xmlhttp = new XMLHttpRequest();
// 	xmlhttp.open("GET", "/php/reLogin.php", true);
// 	xmlhttp.send();
// 	autoCheck = setTimeout("checkLogin()", 2500);
// }

function checkLogin() {
	//var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		// if(this.readyState === 4 && this.status === 200){
		// 	var state = JSON.parse(this.responseText);
		// 	if (state.loginState === 200 )
		// 	window.location.replace("/chat.html");
		// 	else {
		// 	let QRimgEle = document.querySelector("img");
		// 	QRimgEle.setAttribute("src", "/php/QR.png?s=" + Math.random());
		// 	QRimgEle.setAttribute("src", "/php/QR.png" );
		// 	QRimgEle.removeAttribute("style");
		// 	autoCheck = setTimeout("checkLogin()", 500);
		// 	}
		// }

		if (this.readyState === 4 && this.status === 200) {
			var state = JSON.parse(this.responseText);
			if (state.loginState === 200 ) {
				clearTimeout(autoCheck);
				window.location.replace("/chat.html");

			} else if (state.loginState === 201) {
				// clearTimeout(autoCheck);
				// window.location.replace("/chat.html");
				if (Confirmed === 0) {

					document.querySelector('.sub_title').innerHTML = "You didn't log out last time";
					document.querySelector('.sub_desc').innerHTML = "Press Log In will countinue last session";

					let confirmAccount = document.querySelector('.confirm');
					confirmAccount.removeAttribute("style");
					confirmAccount.innerHTML = "Log in";


					let switchAccount = document.querySelector('.switch');
					switchAccount.removeAttribute("style");
					switchAccount.innerHTML = "Switch Account";
				}
				else if (Confirmed === 1) {
					document.querySelector('.sub_title').innerHTML = "Confirm Login on mobile WeChat";
					document.querySelector('.sub_desc').innerHTML = "";
					let confirmAccount = document.querySelector('.confirm');
					confirmAccount.setAttribute("style", "display: none;");

					let switchAccount = document.querySelector('.switch');
					switchAccount.setAttribute("style", "display: none;");
				}
				autoCheck = setTimeout("checkLogin()", 500);

			} else if (state.loginState === 400) {

				document.querySelector('.sub_title').innerHTML = "Scan to log in to WeChat";
				document.querySelector('.sub_desc').innerHTML = "Log in on phone to use WeChat on Web";

				let confirmAccount = document.querySelector('.confirm');
				confirmAccount.setAttribute("style", "display: none;");

				let switchAccount = document.querySelector('.switch');
				switchAccount.setAttribute("style", "display: none;");


				let QRimgEle = document.querySelector("img");
				QRimgEle.setAttribute("src", "/php/QR.png?s=" + Math.random());
				QRimgEle.setAttribute("src", "/php/QR.png" );
				QRimgEle.removeAttribute("style");

				Confirmed = -1;
				autoCheck = setTimeout("checkLogin()", 500);
			}
			// else if (state.loginState === 404) {
			// 	alert('已经保存您上次登录信息，点击确定将会跳转到功能页面')
			// 	window.location.replace("/chat.html");
			// }
			else {
				autoCheck = setTimeout("checkLogin()", 500);
			}
		}
	}
	// xmlhttp.open("GET", "/php/checkLogin.php", true);
	// xmlhttp.send();
	// window.location.replace("/chat.html");
}