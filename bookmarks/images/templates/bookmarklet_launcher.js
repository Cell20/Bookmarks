(function () {
  if (window.mybookmarklet !== undefined) {
    console.log('bookmarklet is defined. Running script');
    mybookmarklet();

  } else {
    let script = document.createElement('script');
    script.src = 'https://mysite.com:8000/static/js/bookmarklet.js?r=' + Math.floor(Math.random() * 99999999999999999999);
    document.body.appendChild(script);
    console.log('bookmarklet is undefined. Creating & appending script');
  }
})();
