function openBlock(e){
    let id = e.target.id;
    let spanText = $(`#${id}.openBlock`);
    let firstSymbol =  spanText.html().slice(0, 1);
    let block = $(`#${id}.block`)

    if (firstSymbol === "+"){
        spanText.html("-" + spanText.html().slice(1));
        block.show();
    }
    else if (firstSymbol === "-"){
        spanText.html("+" + spanText.html().slice(1));
        block.hide();
    }

}


$('.openBlock').on("click", openBlock);