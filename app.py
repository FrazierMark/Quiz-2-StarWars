from flask import Flask, request, render_template
from pprint import PrettyPrinter
import json
import requests

app = Flask(__name__)


STARWARS_URL = 'https://swapi.py4e.com/api/'
pp = PrettyPrinter(indent=4)

starwars_categories = {
    "films": "https://swapi.py4e.com/api/films/",
    "people": "https://swapi.py4e.com/api/people/",
    "planets": "https://swapi.py4e.com/api/planets/",
    "species": "https://swapi.py4e.com/api/species/",
    "starships": "https://swapi.py4e.com/api/starships/",
    "vehicles": "https://swapi.py4e.com/api/vehicles/"
}

@app.route('/')
def homepage():
    """Homepage Route, Show form of Star Wars Categories"""
    category = request.args.get('category')
    context = {
        'starwars_categories': starwars_categories.keys(),
        'indexes': range(1, 15),
    }
    return render_template('home.html', **context)


@app.route('/get_starwars_facts', methods=['GET', 'POST'])
def starwars_search():
    """Show a form to search for GIFs and show resulting GIFs from Tenor API."""
        
    if request.method == 'POST':
        film_list = []
        category = request.form.get('category')
        url = starwars_categories.get(category)
        index = request.form.get('index')
        request_url = url+f'{index}/'
        
        # Gets all starwars data for a given category and index
        response = requests.get(request_url)
        starwars_data = json.loads(response.content)

        
        # Gets all film titles and homeworld for a given person
        if category == 'people' and starwars_data:
            home_world_response = requests.get(starwars_data['homeworld'])
            home_world = json.loads(home_world_response.content)['name']
            
            for film in starwars_data['films']:
                film_list_response = requests.get(film)
                film_list.append(json.loads(film_list_response.content)['title'])
            

        if len(film_list) > 0 and home_world != '':
            context = {
                'category': category,
                'film_list': film_list,
                'home_world': home_world,
                'starwars_data': starwars_data
            }
        else:
            context = {
                'category': category,
                'starwars_data': starwars_data
            }

        return render_template('starwars_results.html', **context)
    else:
        return render_template('home.html')





# if __name__ == '__main__':
#     app.config['ENV'] = 'development'
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

