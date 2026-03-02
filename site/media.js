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
    var media_table_body = document.getElementById("mediagrid");
    for (var element of media_table_body.children){
        if (element.className == "mediaitem"){
            row.style.display = 'block';
        }else{
            row.style.display = 'none';
        }
    }
    for (var tag of tags){
        for (var row of media_table_body.children){
            if (row.className == "mediaitem"){
                continue;
            }
            var row_tags = row.children[5].innerHTML.split(',');
            if (!row_tags.includes(tag)){
                row.style.display = 'none';
            }
        }
    }
}

function reveal_review(slug){
    for (var element of document.getElementsByClassName("content")){
        element.style.display = 'none';
    }
    //console.log(slug)
    //var summary_div = document.getElementById(slug);
    //console.log(summary_div);
    slug.nextElementSibling.style.display = 'block';
}
