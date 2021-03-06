(function () {
  var jquery_version = '3.4.1';
  var site_url = 'https://mysite.com:8000/';
  var static_url = site_url + 'static/';
  var min_width = 100;
  var min_height = 100;

  function bookmarklet(msg) {
    // load CSS
    var css = jQuery('<link>');
    css.attr({
      rel: 'stylesheet',
      type: 'text/css',
      href: static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random() * 99999999999999999999)
    });
    jQuery('head').append(css);
    console.log('css')

    // load HTML
    box_html = '<div id="bookmarklet"><a href="#" onclick="return false;" id="close">&times;</a><h1>Select an image to bookmark:</h1><div class="images"></div></div>';
    jQuery('body').append(box_html);
    console.log('html')


    // close event
    jQuery('#bookmarklet #close').click(function () {
      jQuery('#bookmarklet').remove();
    });

    // find images and display them
    jQuery.each(jQuery('img[src*=".jpg"],[src*=".png"]'), function (index, image) {
      if (jQuery(image).width() >= min_width && jQuery(image).height() >= min_height) {
        // image_url = jQuery(image).attr('src');
        image_url = $(image)[0].src;
        jQuery('#bookmarklet .images').append('<a href="#"><img src="' + image_url + '" /></a>');
      }
    });




    // when an image is selected open URL with it
    jQuery('#bookmarklet .images a').click(function (e) {
      selected_image = jQuery(this).children('img').attr('src');


      // Code to remove the last random numbers from the img url which are used to prevent caching actually forced me to write extra code.
      let newrl
      if (selected_image.includes('.png')) {
        newrl = selected_image.slice(0, selected_image.lastIndexOf(".png") + 4);
      } else if (selected_image.includes('.jpg')) {
        newrl = selected_image.slice(0, selected_image.lastIndexOf(".jpg") + 4);
      }

      console.log(newrl);



      // selected_image = $('img')[0].src;
      // hide bookmarklet
      jQuery('#bookmarklet').hide();
      // open new window to submit the image
      window.open(site_url + 'images/create/?title=' + encodeURIComponent(jQuery('title').text()) + '&url=' + encodeURIComponent(newrl), '_blank');
    });
  };

  // Check if jQuery is loaded
  if (typeof window.jQuery != 'undefined') {
    bookmarklet();
  } else {
    var conflict = typeof window.$ != 'undefined'; // Check for conflicts
    // Create the script and point to Google API
    var script = document.createElement('script');
    script.src = '//ajax.googleapis.com/ajax/libs/jquery/' + jquery_version +
      '/jquery.min.js';
    console.log('loaded')
    document.head.appendChild(script); // Add the script to the 'head' for processing

    // create a way to wait until script loading
    var attempts = 15;
    (function () {
      // Check again if jQuery is undefined
      if (typeof window.jQuery == 'undefined') {
        if (--attempts > 0) {
          // Calls himself in a few milliseconds
          window.setTimeout(arguments.callee, 250)
        } else {
          // Too much attempts to load, send error
          alert('An error occurred while loading jQuery')
        }
      } else {
        bookmarklet();
      }
    })();
  }
})()
