
    // AJAX / JQuery POST request execution tbd.
    const pathRegex = /from:\s(.+)\suploaded/;
    const fileRegex = /File\s(.+)\sfrom/;

    function share(file) {
        var match = file.match(pathRegex);
        var matchFile = file.match(fileRegex);
        console.log(match[1]);
        var r = new XMLHttpRequest();
        r.open("POST", "http://0.0.0.0:5000/share", true);
        r.onreadystatechange = function () {
            if (r.readyState != 4 || r.status != 200) return;
            //alert("Success: " + r.responseText);
            console.log("sent");
        };
        r.send(JSON.stringify({"input": match[1]}));
        alert(`Your file will be available here: 0.0.0.0:5000/file/${matchFile[1]}`)

    }

   // alert("test");
