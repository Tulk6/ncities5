function reveal_issue(){
    var background_audio = document.getElementById("background_audio");
    var issue_content = document.getElementById("issue_content");
    var reveal_button = document.getElementById("reveal_button");
    
    console.log("hello!");
    background_audio.play();
    issue_content.style.display = "block";
    reveal_button.style.display = "none";
}

function mute_audio(){
    var background_audio = document.getElementById("background_audio");
    var mute_button = document.getElementById("mute_button");
    background_audio.muted = !background_audio.muted;
    mute_button.innerHTML = background_audio.muted ? "UNMUTE" : "MUTE"
}
