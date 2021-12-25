let sizeBtn = document.getElementsByClassName('btn-size')
let addQuantity = document.getElementById('AddQty')
let removeQuantity = document.getElementById('RemoveQty')
let QuantityInput = document.getElementById('Qty')
let spanQty = document.getElementById('spanQty')

addQuantity.addEventListener('click',()=>{
    let Val = parseInt(QuantityInput.value)
    let spanVal = parseInt(spanQty.innerText)
    QuantityInput.value = Val + 1;
    spanQty.innerText = QuantityInput.value 
})

removeQuantity.addEventListener('click',()=>{
    let Val = parseInt(QuantityInput.value)
    let spanVal = parseInt(spanQty.innerText)
    if(Val > 1){
        QuantityInput.value = Val - 1;
        spanQty.innerText = QuantityInput.value 
    }
})


for(btn of sizeBtn){
    btn.addEventListener('click', function() {
        console.log('You selected: ', this.innerText);
        for(let btn of sizeBtn){
            btn.classList.remove('selected')
        }
        this.classList.add('selected')
        document.getElementById('add-cart').value =  this.innerText.toLowerCase()
        document.getElementsByClassName('btn-add-size')[0].removeAttribute('disabled')

    });
}

console.log(sizeBtn)