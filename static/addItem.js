let sizeBtn = document.getElementsByClassName('btn-size')


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