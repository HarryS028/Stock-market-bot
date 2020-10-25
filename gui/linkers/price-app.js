let {PythonShell} = require('python-shell')
var path = require("path")
const fs = require('fs')

function test() {
    alert("HEEL")
}

function login() {

    var key = document.getElementById("key").value
    var username = document.getElementById("username").value
    var password = document.getElementById("password").value

    let data = [key, username, password]

    fs.writeFile('linkers/data.txt', data, (err) => { 
        if (err) throw err; 
    }) 

}

function get_data() {

    var str = fs.readFileSync('data.txt', 'utf8');

    alert(str)

    // var options = {
    //     scriptPath: path.join(__dirname, '/../engine/'),
    //     args: [key, username, password]
    // }

    // let pyshell = new PythonShell('historical-prices.py', options);

    // pyshell.on('message', function(message) {
    //     alert(message);
    // })

    // alert(key)

}

