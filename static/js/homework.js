

var subbtn = document.getElementById("js_submit_seeas");
var jxbox = document.getElementsByClassName("homework_jxbox");
var sebtn = document.getElementsByClassName("sebtn");
console.log(sebtn);


for(var j=0;j<sebtn.length;j++){
    sebtn[j].onclick = function () {
        console.log(this.style.backgroundColor);
        if(this.style.backgroundColor =="red"){
            console.log("1");
            this.style.backgroundColor = "#ffffff";
            this.classList.remove("choosed");
        }else {
            this.style.backgroundColor = "red";
            this.classList.add("choosed")
        }

    }
}




subbtn.onclick = function () {
    var choosedbtn = document.getElementsByClassName("choosed");//选择的数组，可用[].innerHTML
    var tureanswerbox = document.getElementsByClassName("js_jxbox");
    // var tureanswer = tureanswerbox[0].getElementsByTagName("span");
    // var tureanswertwo = tureanswerbox[1].getElementsByTagName("span");

    var rorf = document.getElementsByClassName("right_or_false");

    for(var k=0;k<choosedbtn.length;k++){
        console.log(choosedbtn[k].innerHTML);
        console.log(tureanswerbox[k].getElementsByTagName("span")[0].innerHTML);
        tureanswerbox[k].getElementsByTagName("p")[0].innerHTML = choosedbtn[k].innerHTML;
        if(choosedbtn[k].innerHTML == tureanswerbox[k].getElementsByTagName("span")[0].innerHTML){
            console.log(1);
        }else {
            console.log(0);
            rorf[k].innerHTML = "回答错误"
            rorf[k].style.color = "red";
        }
    }
    for(var i=0;i<jxbox.length;i++){
        jxbox[i].style.display = 'block';
    }
    this.style.display = 'none';
}