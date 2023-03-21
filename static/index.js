const blog_card = document.querySelector('.blog-cards');



blog_card.addEventListener('click', ()=>{
    window.location.href ="/blog-content";
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





// git clone https://github.com/Surajsinhar77/blog_post.git