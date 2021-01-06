/*if (window.location.href == "http://127.0.0.1:5000/account")*/

function nonStandart(string, chkstr){
	if (string.length > 0){
		for (var i_counter = 0; i_counter < string.length; i_counter++){
			for (var j_counter = 0; j_counter < chkstr.length; j_counter++){
				if (string[i_counter] == chkstr[j_counter]) return false;
			}
		}
	}
	else return false;
	return true;
}


function checkRight(read, ans, val1, val2, val3, val4) {
	var help = document.getElementById(read).value;
	var answer = document.getElementById(ans);
	if (nonStandart(help, "!/,#$") == true && help != null){
		answer.style.color = "green";
		answer.innerHTML = "OK!"; 
	}
	else {
		answer.style.color = "red";
		answer.innerHTML = "X";
	}
	for (var i_counter=1; i_counter <= 4; i_counter++){
		if (document.getElementById("val"+i_counter.toString()).innerHTML != "OK!"){
			document.getElementById("bt").disabled = true;
		} 
	}
	document.getElementById("bt").disabled = false;
}

function checkPass(read, orig, ans, val1, val2, val3, val4){
	var original = document.getElementById(orig).value;
	var help = document.getElementById(read).value;
	var answer = document.getElementById(ans);
	if (help == original && help != "" && help != null) {
		answer.style.color = "green";
		answer.innerHTML = "OK!";
	}
	else {
		answer.style.color = "red";
		answer.innerHTML = "X"; 
	}
	for (var i_counter=1; i_counter <= 4; i_counter++){
		if (document.getElementById("val"+i_counter.toString()).innerHTML != "OK!"){
			document.getElementById("bt").disabled = true;
		} 
	}
	document.getElementById("bt").disabled = false;
}
