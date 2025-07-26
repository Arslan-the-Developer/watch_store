document.addEventListener('DOMContentLoaded', () => {

    let navDropdown = document.getElementById("nav_dropdown");
    let shopLink = document.getElementById("shop_link");
    let searchForm = document.getElementById("search_form");
    let nav_open_button = document.getElementById('nav_open_menu');
    let nav_close_button = document.getElementById('nav_close_button');
    let nav_menu = document.getElementById('nav_menu');

    let dropdownTimeout;

    function showDropdown() {
        clearTimeout(dropdownTimeout);
        navDropdown.classList.remove('hidden');
        requestAnimationFrame(() => {
            navDropdown.classList.remove('opacity-0');
        });
    }

    function hideDropdown() {
        navDropdown.classList.add('opacity-0');
        dropdownTimeout = setTimeout(() => {
            navDropdown.classList.add('hidden');
        }, 300); // matches duration-300
    }

    shopLink.addEventListener('mouseenter', showDropdown);
    shopLink.addEventListener('mouseleave', hideDropdown);

    navDropdown.addEventListener('mouseenter', showDropdown);
    navDropdown.addEventListener('mouseleave', hideDropdown);

    searchForm.addEventListener('submit', (e) => {
        
        e.preventDefault();

        let form_data = new FormData(e.target);
        const searchValue = form_data.get('search_value').trim(); // Remove spaces
        const searchInput = document.querySelector('input[name="search_value"]');
        const ElemntToWorkWith = document.querySelector('input[name="search_value"]').parentElement;


         if (searchValue === '') {
            // Input is empty — show red background
                ElemntToWorkWith.style.borderColor = '#cf0000'; // Tailwind's red-300
                searchInput.setAttribute('placeholder','Should Not Be Empty'); // Tailwind's red-300

                setTimeout(() => {

                    ElemntToWorkWith.style.borderColor = '#345635'; // Tailwind's red-300
                    searchInput.setAttribute('placeholder','Search Luxury'); // Tailwind's red-300
                    
                }, 1500);
                return; // Stop further execution

            } else {
                
                window.location.href = `/search/${searchValue}`;

            }
    });


    nav_open_button.addEventListener('click', ()=> {

      nav_menu.classList.remove('-top-100');
      nav_menu.classList.add('top-0');

    });
    
    nav_close_button.addEventListener('click', ()=> {

      nav_menu.classList.remove('top-0');
      nav_menu.classList.add('-top-100');

    });


});


async function AddProductToCart(e, product_id) {

    e.target.setAttribute('disabled',true);

  try {
    const response = await fetch('/manage-cart-product', {
      method: "POST",
      body: JSON.stringify({ prod_id: product_id }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken() // ✅ Correct header
      }
    });

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    console.log(json);
  } catch (error) {
    console.error(error.message);
  }
}




async function AddProductTowishlist(e, product_id) {

    e.target.setAttribute('disabled',true);

  try {
    const response = await fetch('/manage-wishlist-product', {
      method: "POST",
      body: JSON.stringify({ prod_id: product_id }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCSRFToken() // ✅ Correct header
      }
    });

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const json = await response.json();
    console.log(json);
  } catch (error) {
    console.error(error.message);
  }

  e.target.setAttribute('disabled',false);

}


function getCSRFToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');

  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.slice(name.length + 1));
    }
  }

  return null;
}
