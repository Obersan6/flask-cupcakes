// Query the API to get the cupcakes and add to the page.
// Handle form submission to both let the API know about the new cupcake and updates the list on the page to show it.

const apiURL = 'http://127.0.0.1:5000/api/cupcakes';

const ul = $('#cupcake-list');
const form = $('#add-cupcake-form');

// Function to create a list item for a cupcake
function appendCupcake(cupcake) {
    let cupcakeFlavor = `<li>${cupcake.flavor}</li>`;
    ul.append(cupcakeFlavor);
}

// Retrieve and append cupcakes by flavor
async function getCupcakes() {
    try {
        const response = await axios.get(apiURL);
        const cupcakes = response.data.cupcakes;

        // Loop through the cupcakes and append each flavor to the list
        for (let cupcake of cupcakes) {
            appendCupcake(cupcake);
        }
    } catch (error) {
        console.error("Error fetching cupcakes:", error);
    }
}

// Call the function to get and display cupcakes
getCupcakes();

// Event listener for form submission
form.on('submit', async function(event) {
    event.preventDefault();

    // Get form data
    const flavor = $('#flavor').val();
    const size = $('#size').val();
    const rating = $('#rating').val();
    const image = $('#image').val();

    // Create new cupcake via API
    try {
        const response = await axios.post(apiURL, {
            flavor: flavor,
            size: size,
            rating: rating,
            image: image
        });

        // Append the newly created cupcake to the list
        appendCupcake(response.data.cupcake);

        // Clear the form fields
        form.trigger('reset');
    } catch (error) {
        console.error("Error adding cupcake:", error);
    }
});
