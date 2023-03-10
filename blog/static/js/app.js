const preview = document.getElementById("preview");
const textbox = document.getElementById("markdown-box");


var pre = ""

function set_timer() {
	return setInterval(() => {
		if (pre == textbox.value) return;

		fetch("/markapi/", {
			method: "POST",
			headers: {
				"Accept": "application/json",
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ mdtext: textbox.value }),
		})
			.then((response) => response.json())
			.then((data) => (preview.innerHTML = data.html));
		
		pre = textbox.value;

	}, 500);
}


var timer = set_timer();


textbox.addEventListener("input", () => {
	console.log("H");
	clearInterval(timer);
	timer = set_timer();
})