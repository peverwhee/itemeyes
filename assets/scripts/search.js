$("#search-form").submit(function(event) {
	//console.log("butts");
	event.preventDefault();

	var form = $(this);
	var item = form.find('input[name="item-name"]').val();
	var city = form.find('input[name="city-name"]').val();
	console.log(item);

	$.ajax({
		method: "POST",
		url: "http://localhost" + form.attr('action'),
		data: JSON.stringify({
			item: item,
			city: city
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