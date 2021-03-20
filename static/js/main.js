class View {
   static addToPage(element, component) {
        $(element).append(component)
    }
}

class Cupcake {
    
    default_image = "https://tinyurl.com/demo-cupcake"

    constructor(id, flavor, size, image, rating) {
        if (!image) this.image = this.default_image;

        this.id = id
        this.flavor = flavor;
        this.size = size;
        this.image = image;
        this.rating = rating;
    }

    buildViewComponent() {
        console.log(this.image)
        return $(`
            <li>
                <div class="card" style="width: 18rem;">
                    <img src="${this.image}" class="card-img-top" alt="${this.flavor}">
                    <div class="card-body">
                    <h5 class="card-title">${this.flavor}</h5>
                    <p class="card-text">Size: ${this.size}</p>
                    <p class="card-text">Rating: ${this.rating}</p>
                    </div>
                </div>
            </li>
        `)
    }
}

function main() {
    axios.get('http://localhost:5000/api/cupcakes')
    .then(({data}) => {
        const cupcakeComponents = data.cupcakes
                .map(cupcakeJson => Object.assign(new Cupcake(), cupcakeJson))
                .map(cupcake => cupcake.buildViewComponent());
        
        View.addToPage('.cupcakes-list', cupcakeComponents);
    })
    .catch((error) => {
        console.log(error)
    })
}

$( document ).ready(function() {
    main();
});