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


function checkRight(read, ans) {
	var help = document.getElementById(read).value;
	var answer = document.getElementById(ans);
	if (nonStandart(help, "!/.,#$1234567890") == true){
		answer.style.color = "green";
		answer.innerHTML = "OK!";
		document.getElementById("bt").disabled = false; 
	}
	else {
		answer.style.color = "red";
		answer.innerHTML = "X";
		document.getElementById("bt").disabled = true; 
	}
}

