from flask import Flask, render_template, request, send_from_directory
import openai
import json
import os


app = Flask(__name__)

@app.route('/response/<filename>')
def response(filename):
    return send_from_directory('response', filename)

@app.route('/')
def home():
    return render_template('CookAI.html')

@app.route('/kitchen')
def kitchen():
    return render_template('Kitchen — CookAI.html')

@app.route('/fridge')
def fridge():
    return render_template('Fridge — CookAI.html')

@app.route('/generate', methods=['POST'])
def generate():
    api_key = request.form['api_key']
    user_input = request.form['user_input']

    # Check for API key and user input
    if not api_key:
        return "API key is required", 400
    if not user_input:
        return "User input is required", 400
    
    # Construct the prompt for the OpenAI API
    prompt_part0 = "We are creating a recipe. The output should be in JSON format with specific sections with no additonal comments. "
    prompt_part1 = "The JSON structure should include 'title', 'serving_size', 'ingredients', and 'instructions' in that order. "
    prompt_part2 = "Start with a 'title' section, followed by 'serving_size'. Then, 'serving_size' should be 4. "
    prompt_part3 = "Next, list 'ingredients' without sesame seeds and peanuts due to allergies. "
    prompt_part4 = ("Finally, provide 'instructions' as an ordered list of steps. You do not have to use all the ingredients in the following list. "
                    "Only use what you need for the recipe. If the following list does not include an ingredient, do NOT include it. "

                    "Here is the list of ingredients to choose from: "
                    "Potatoes, Onions, Bell Pepper, Carrots, Lettuce, Spinach, Celery, Tomatoes, Jalapeños, Broccoli, "
                    "Cauliflower, Cucumber, Zucchini, Mushrooms, Green beans, Radishes, Corn, Asparagus, Peas, Eggplant, "
                    "Black Beans, Garbanzo Beans, White Rice, Angel Hair Pasta, Brown Sugar, Peanuts, Sesame Seeds, Lentils, Quinoa, Almonds, "
                    "Walnuts, Flaxseeds, Chia seeds, Sunflower seeds, Rolled oats, Farro, Couscous, Buckwheat, Hemp seeds, "
                    "Dill, Cumin, Smoked Paprika, Cayenne, Oregano, Salt, Pepper, Basil, Parsley, Rosemary, "
                    "Thyme, Garlic powder, Onion powder, Chili powder, Turmeric, Coriander, Bay leaves, Cinnamon, Nutmeg, Ginger, "
                    "Tortilla Wrap, Sliced White Bread, Flatbread, Croissant, Bagel, Biscuit, Hamburger Bun, Hot Dog Roll, White Sub Roll, Whole wheat tortilla wrap, "
                    "Multigrain bread, Pita bread, Naan, English muffin, Ciabatta roll, Pretzel bun, Rye bread, Sourdough bread, French baguette, "
                    "Vinegar, Tomato Paste, Olive Oil, Canola Oil, Ketchup, Lemon, Lime, Soy sauce, Honey, Mustard, "
                    "Worcestershire sauce, Hot sauce, Balsamic glaze, Sesame oil, Fish sauce, Maple syrup, Apple cider vinegar, Barbecue sauce, Mayonnaise, "
                    "Chicken Wings, Shredded Beef, Salmon, Eggs, Milk, Butter, Shredded Cheddar Cheese, Parmesan, Yogurt, Ground beef, "
                    "Turkey breast, Tofu, Pork chops, Shrimp, Tuna, Lentils, Chickpeas, Tempeh, Quinoa, Cottage Cheese. "

                    "Please format the ingredients as a JSON object. ")
    prompt_part5 = "The food I want to make is: "

    # Combine all the parts to create the final prompt
    final_prompt = prompt_part0 + prompt_part1 + prompt_part2 + prompt_part3 + prompt_part4 + prompt_part5 + user_input

    try:
        # Create an OpenAI client instance
        client = openai.OpenAI(api_key=api_key)
        
        # Generate a chat completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": final_prompt}],
            model="gpt-3.5-turbo"
        )
        
        # Extract the generated text
        generated_text = response.choices[0].message.content
    except Exception as e:
        # Return an error if something goes wrong
        return f"An error occurred: {str(e)}", 500

    # Check and create the 'response' directory if it does not exist
    directory = os.path.join(app.root_path, 'response')
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Save the generated text to a JSON file in the 'response' folder
    file_path = os.path.join(directory, 'out.json')
    with open(file_path, 'w') as outfile:
        json.dump({'generated_text': generated_text}, outfile)

    # Return the generated text to the client by rendering a template
    return render_template('generate — CookAI.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)
