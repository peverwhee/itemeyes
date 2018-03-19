window.onload = function() {
	var token = localStorage.getItem("token");
	if (token === null || token === "") {
		window.location.replace("/login.html");
	}
}

$("#search-form").submit(function(event) {
	event.preventDefault();

	var form = $(this);
	var brand = form.find('input[name="brand-name"]').val();
	var zip = form.find('input[name="zip-name"]').val();
	var model = form.find('input[name="model-name"]').val();
	if (!model)
	{
		model = null
	}
	$.ajax({
		method: "POST",
		url: "http://localhost" + form.attr('action'),
		data: JSON.stringify({
			brand: brand,
			model: model,
			zip: zip
		})
	})
	.done(function(response) {
		//response is what's written (string) from itemeyes.py (wfile.write)
		showSearchResults(response);
	})
	.fail(function(error) {
		console.log(error);
	});
})

$("#add-form").submit(function(event) {
	event.preventDefault();

	var form = $(this);
	var brand = form.find('input[name="brand-name-add"]').val();
	var model = form.find('input[name="model-name-add"]').val();
	if (!model)
	{
		model = null
	}
	var company = form.find('input[name="company-name-add"]').val();
	var city = form.find('input[name="city-name-add"]').val();
	var state = form.find('input[name="state-name-add"]').val();
	var zip = form.find('input[name="zip-name-add"]').val();
	var address = form.find('input[name="address-name-add"]').val();
	var token = localStorage.getItem("token");
	$.ajax({
		method: "POST",
		url: "http://localhost" + form.attr('action'),
		data: JSON.stringify({
			brand: brand,
			model: model,
			company: company,
			address: address,
			city: city,
			state: state,
			zip: zip,
			token: token
		})
	})
	.done(function(response) {
		//response is what's written (string) from itemeyes.py (wfile.write)
		addItem(response);
	})
	.fail(function(error) {
		console.log(error);
	});
})

function addItem(response) {
	console.log(response);
	results = "<p> Item added! </p>";
	$("#add-success").html(results);
}

function showSearchResults(response) {
	console.log(response);
	var jsonData = JSON.parse(response);
	var table = "<table> <tr> <th> Company </th> <th> Location </th> </tr>";
	var rows = jsonData.rows;
	console.log(rows);
	var row;
	for (let i=0; i<rows.length; i++) {
		console.log(rows[i].company)
		table += "<tr> <td>" + rows[i].company + "</td> <td>" + rows[i].location + "</td> </tr>";
	}
	table += "</table>";
	$("#item-search-results").html(table);
}

function logoutButtonClick() {
	localStorage.removeItem('token');
	window.location.replace('/login.html');
}

