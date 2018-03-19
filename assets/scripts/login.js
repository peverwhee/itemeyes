window.onload = function() {
	var token = localStorage.getItem("token");
	if (token != null && token != "" && token != undefined) {
		window.location.replace("/index.html");
	}
}

$("#login-form").submit(function(event) {
	event.preventDefault();

	var form = $(this);
	var username = form.find('input[name="username-name"]').val();
	var pass = form.find('input[name="pass-name"]').val();
	var passHash = hash(pass);
	$.ajax({
		method: "POST",
		url: "http://localhost" + form.attr('action'),
		data: JSON.stringify({
			username: username,
			passHash: passHash,
		})
	})
	.done(function(response) {
		//response is what's written (string) from itemeyes.py (wfile.write)
		login(response, "login");
	})
	.fail(function(error) {
		console.log(error);
	});
})

$('#create-account-form').submit(function(event) {
	event.preventDefault();
	var form = $(this);
	var first = form.find('input[name="first-name"]').val();
	var last = form.find('input[name="last-name"]').val();
	var username = form.find('input[name="username-name-create"]').val();
	var pass1 = form.find('input[name="pass1-name"]').val();
	var pass2 = form.find('input[name="pass2-name"]').val();
	if (pass1 != pass2) {
		$("#create-fail").html("<p> Passwords do not match! </p>");
		return;
	}
	var passHash = hash(pass1);
	$.ajax({
		method: "POST",
		url: "http://localhost" + form.attr('action'),
		data: JSON.stringify({
			firstName: first,
			lastName: last,
			username: username,
			passHash: passHash,
		})
	})
	.done(function(response) {
		//response is what's written (string) from itemeyes.py (wfile.write)
		login(response, "create");
	})
	.fail(function(error) {
		console.log(error);
	});
})

function hash(password) {
	var hash = 0;
	if (password.length == 0) {
		return hash;
	}
	for (var i = 0; i < password.length; i++) {
		char = password.charCodeAt(i);
		hash = ((hash<<5)-hash) + char;
		hash = hash & hash;
	}
	hash = hash.toString();
	return hash;
}

//console.log(hash("car0line"));

function login(response, action) {
	// save username in local storage
	console.log(response);
	var jsonData = JSON.parse(response);
	var token = jsonData.token;
	if (token == "") {
		if (action =="login") {
			$("#login-fail").html("<p> Username/Password combination invalid! </p>");
		}
		else if (action == "create") {
			$("#create-fail").html("<p> Username already exists! </p>");
		}
		return;
	}
	localStorage.setItem("token", token);
	window.location.replace("/index.html");
}
