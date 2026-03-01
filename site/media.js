function update_filters(){
    var filter_form = document.getElementById("filterdiv");
    var tags = [];
    for (var child of filter_form.childNodes){
        if (child.nodeName != "LABEL"){
            continue;
        }
        var checked = child.firstChild.checked;
        if (checked){
            if (child.textContent == "all"){
                tags = [];
            }else{
                tags.push(child.textContent);
            }
        }
    }
    filter_media(tags);
}

function filter_media(tags){
    var media_table_body = document.getElementById("mediatablebody");
    for (var row of media_table_body.children){
        if (row.className == "mediasummary"){
            row.style.display = 'table-row';
        }else{
            row.style.display = 'none';
        }
    }
    for (var tag of tags){
        for (var row of media_table_body.children){
            if (row.className == "mediacontent"){
                continue;
            }
            var row_tags = row.children[5].innerHTML.split(',');
            if (!row_tags.includes(tag)){
                row.style.display = 'none';
            }
        }
    }
}

function reveal_review(title){
    for (var element of document.getElementsByClassName("mediacontent")){
        element.style.display = 'none';
    }
    var summary_row = document.getElementById(title);
    console.log(summary_row);
    summary_row.nextElementSibling.style.display = 'table-row';
}
