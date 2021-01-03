function checkEmail(string) 
{
	return string.lastIndexOf('.') - string.indexOf('@') > 0;
}

function checkFormInfo()
{

	var login = document.getElementById("login").value;
	var password = document.getElementById("password").value;

	var params = {login: encodeURIComponent(login), password: encodeURIComponent(password)};
	fetch('http://127.0.0.1:5000/login', {
			method: "POST",
			redirect: "main",
			body: JSON.stringify(params),
			headers: new Headers({
			"content-type": "application/json"
    		})
		});

	event.preventDefault();
	return 0;
}