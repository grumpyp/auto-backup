
    // AJAX / JQuery POST request execution tbd.
    const fileRegex = /File(.+)uploaded/;

    function share(file) {
        console.log(file)
        var match = file.match(fileRegex);
        console.log(match[1]);

    }

   // alert("test");
