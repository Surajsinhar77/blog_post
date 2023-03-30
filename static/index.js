const blog_card = document.querySelectorAll('.blog-cards');

// let a = 1;
blog_card.forEach((item)=>{
    item.addEventListener('click', ()=>{
        let title_data = item.querySelector('.card-title').textContent;
        window.location.href = `/blog-content?title=${title_data}`;
    })

})


function ellipsify(str) {
    if (str.length > 10) {
        return (str.substring(0, 80) + "...");
    }
    else {
        return str;
    }
}

let cardTextAll = document.querySelectorAll('.blog-content-home');

cardTextAll.forEach(element => {
    element.innerHTML = ellipsify(element.textContent);
});

let getMsg = document.querySelector('.error_msg');
let getMsgchange = document.querySelector('.error_msg').textContent;

getMsg.addEventListener('change',()=>{
    setTimeout(()=>{
        console.log("can u come here")
        getMsg.style.display = 'none';
    },2000)
})




// git clone https://github.com/Surajsinhar77/blog_post.git