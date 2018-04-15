
var isLogout = false;
var isUpdateFriend;

var autoReplyStatus = 0;

var autoCheckNew;

var chosenChatroom = new Array();

// function autoReply() {
// 	if (autoReplyStatus === 0) {
// 		var xmlhttp = new XMLHttpRequest();
// 		xmlhttp.onreadystatechange = function() {
// 			if (this.readyState === 4 && this.status === 200) {
// 				let autoReplyButton = document.querySelector("#autoReplyButton");
// 				autoReplyButton.setAttribute("onclick", "autoReply();");
// 				autoReplyButton.innerHTML = "Stop Robot";
// 				autoReplyStatus = 1;
// 				let infoEle = document.querySelector("#robotInfo");
// 				infoEle.innerHTML = "Robot is running."
// 			}
// 		}
// 		xmlhttp.open("GET", "/php/startReply.php", true);
// 		xmlhttp.send();
// 	} else {
// 		var xmlhttp = new XMLHttpRequest();
// 		xmlhttp.onreadystatechange = function() {
// 			if (this.readyState === 4 && this.status === 200) {
// 				let autoReplyButton = document.querySelector("#autoReplyButton");
// 				autoReplyButton.setAttribute("onclick", "autoReply();");
// 				autoReplyButton.innerHTML = "Start Robot";
// 				autoReplyStatus = 0;
//
// 				let infoEle = document.querySelector("#robotInfo");
// 				infoEle.innerHTML = "Robot is stopped."
// 			}
// 		}
// 		let autoReplyButton = document.querySelector("#autoReplyButton");
// 		autoReplyButton.removeAttribute("onclick");
// 		autoReplyButton.innerHTML = "Stopping...";
// 		xmlhttp.open("GET", "/php/stopReply.php", true);
// 		xmlhttp.send();
//
// 	}
//
// }

function flipChoice(num) {
	chosenChatroom[num] = 1 - chosenChatroom[num];
	if (chosenChatroom[num] === 0) {
		let chatroomLi = document.querySelector("#chatroom" + num);
		chatroomLi.removeAttribute("class");
	} else {
		let chatroomLi = document.querySelector("#chatroom" + num);
		chatroomLi.setAttribute("class", "chatroom_1");
	}
}

function checkRobotStatus() {

	var xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function() {
		if (this.readyState === 4 && this.status === 200) {
			if (this.responseText === "0") {
				let autoReplyButton = document.querySelector("#autoReplyButton");
				autoReplyButton.setAttribute("onclick", "autoReply();");
				autoReplyButton.innerHTML = "Start Robot";
				autoReplyStatus = 0;
				let infoEle = document.querySelector("#robotInfo");
				infoEle.innerHTML = "Robot is stopped."
			}
			else {
				let autoReplyButton = document.querySelector("#autoReplyButton");
				autoReplyButton.setAttribute("onclick", "autoReply();");
				autoReplyButton.innerHTML = "Stop Robot";
				autoReplyStatus = 1;
				let infoEle = document.querySelector("#robotInfo");
				infoEle.innerHTML = "Robot is running."
			}
		}
	}
	xmlhttp.open("GET", "/php/checkRobotStatus.php", true);
	let infoEle = document.querySelector("#robotInfo");
	infoEle.innerHTML = "Updating robot status..."
	xmlhttp.send();

}

function checkNew() {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if (this.readyState === 4 && this.status === 200) {
			let newFriends = JSON.parse(this.responseText);
			if (newFriends.length > 0) {
				let infoEle = document.querySelector("#friendInfo");
				infoEle.innerHTML = "";
				for (let i = 0; i < newFriends.length; i++) {
					let friendLi = document.createElement("li");
					friendLi.innerHTML = newFriends[i] + " is your friend now.";
					infoEle.appendChild(friendLi);
				}
			}
			if (isLogout) return;

			if (isUpdateFriend === false) {
				autoCheckNew = setTimeout("checkNew();", 500);
			}
		}
	}
	xmlhttp.open("GET", "/php/checkNew.php", true);
	xmlhttp.send();
}

function updateFriendList() {

	if (isLogout) return;
	var xmlhttp = new XMLHttpRequest();

	xmlhttp.onreadystatechange = function() {
		if (this.readyState === 4 && this.status === 200) {

			let infoEle = document.querySelector("#friendInfo");
			infoEle.innerHTML = "Friend list has updated.";
			autoCheckNew = setTimeout("checkNew();", 500);
			isUpdateFriend = false;
		}
	}

	xmlhttp.open("GET", "/php/updateFriendList.php", true);
	xmlhttp.send();


}

function updateChatroom() {
	if (isLogout) return;

	let autoReplyButton = document.querySelector("#autoReplyButton");
	autoReplyButton.removeAttribute("onclick");

	let updateButton = document.querySelector("#updateButton");
	updateButton.removeAttribute("onclick");

	let addButton = document.querySelector("#addButton");
	addButton.removeAttribute("onclick");

	let chatroomsEle = document.querySelector('#chatrooms');
	chatroomsEle.innerHTML = "... ... ...";


	checkRobotStatus();

	isUpdateFriend = true;
	let friendInfoEle = document.querySelector("#friendInfo");
	friendInfoEle.innerHTML = "Updating friend list...";
	clearTimeout(autoCheckNew);
	setTimeout("updateFriendList();", 5000);

	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {

		if (this.readyState === 4 && this.status === 200) {
			if (isLogout) return;
			let chatrooms = JSON.parse(this.responseText);
			let chatroomsEle = document.querySelector('#chatrooms');
			chatroomsEle.innerHTML = "";
			for (let i = 0; i < chatrooms.length; i++) {
				if (isLogout) return;

				let chatroomLi = document.createElement("li");
				chatroomLi.setAttribute("id", "chatroom" + i);
				chatroomLi.setAttribute("onclick", "flipChoice(" + i + ");");
				chatroomLi.innerHTML = chatrooms[i];
				chatroomsEle.appendChild(chatroomLi);

				chosenChatroom[i] = 0;
			}

			if (isLogout) return;
			
			let infoEle = document.querySelector("#chatroomInfo");
			infoEle.firstChild.innerHTML = "Chatroom list has been updated.";

			let autoReplyButtonR = document.querySelector("#autoReplyButton");
			autoReplyButtonR.setAttribute("onclick", "autoReply();");

			let updateButtonR = document.querySelector("#updateButton");
			updateButtonR.setAttribute("onclick", "updateHandler();");

			let addButtonR = document.querySelector("#addButton");
			addButtonR.setAttribute("onclick", "addFriendsHandler();");
			
		}
	}
	if (isLogout) return;
	xmlhttp.open("GET", "/php/updateChatroom.php", true);
	xmlhttp.send();


	let infoEle = document.querySelector("#chatroomInfo");

	infoEle.innerHTML = "";
	let infoP = document.createElement("p");
	infoP.innerHTML = "Updating chatroom list...";
	infoEle.appendChild(infoP);

}

function updateHandler() {

	updateChatroom();
}

function addFriends(chatroom) {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.onreadystatechange = function() {
		if (this.readyState === 4 && this.status === 200) {
			
			let infoEle = document.querySelector("#chatroomInfo");
			infoEle.firstChild.innerHTML = "Done.";
			let addLi = document.createElement("li");
			addLi.innerHTML = "Friend requests for <span style='font-weight: bold;'>" + chatroom + "</span> have been sent.";
			infoEle.appendChild(addLi);
		}
	}
	xmlhttp.open("GET", "/php/addFriends.php?add=" + chatroom, true);
	let infoEle = document.querySelector('#chatroomInfo');
	infoEle.firstChild.innerHTML = "Sending friend requests for <span style='font-weight: bold;'>" + chatroom + "</span>...";
	xmlhttp.send();
}

function addFriendsHandler() {
	for (let i = 0; i < chosenChatroom.length; i++) {
		if (isLogout) return;
		if (chosenChatroom[i] === 1) {
			let chatroomLi = document.querySelector("#chatroom" + i);
			addFriends(chatroomLi.innerHTML);
		}
		chosenChatroom[i] = 0;
		let chatroomLi = document.querySelector("#chatroom" + i);
		chatroomLi.removeAttribute("class");
	}
}


function logoutHandler() {
	isLogout = true;
	clearTimeout(autoCheckNew);
	setTimeout("logout()", 5000);
	document.querySelector("body").innerHTML = "<h3>Cleaning up...</h3>";
}


function logout() {
	var xmlhttp = new XMLHttpRequest();
	xmlhttp.open("GET", "/php/logout.php", true);
	xmlhttp.send();
	xmlhttp.onreadystatechange = function() {
		if (this.readyState === 4 && this.status === 200) {
			if (confirm("Do you want to re-login?")) {
				window.location.replace("/index.html");
			}
			else {
				document.querySelector("body").innerHTML = "<h3>Bye~</h3>";
			}
		}
	}


}