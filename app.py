from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

data = {
    'Activity': ['TV', 'Driving', 'Flying', 'Biking', 'Walking'],
    'CO2_Emission': [0.001, 0.24, 0.15, 0.008, 0.001]
}
emission_dict = {
    'Swimming': 0.01,
    'Driving' : 0.24,
    'Flying' : 0.15,
    'Biking' : 0.008,
    'Walking':0.001

}
emissions_df = pd.DataFrame(data)

def estimate_carbon_footprint(activity, distance, people=1):
    #emission = emissions_df.loc[emissions_df['Activity'] == activity, 'CO2_Emission'].values[0]
    emission = emission_dict.get(activity,None)
    print(emission)
    carbon_footprint = emission * distance * people
    return carbon_footprint

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    activity = request.form["activity"]
    distance = float(request.form["distance"])
    people = int(request.form["people"])
    result = compare(activity, distance, people)
    return jsonify(carbon_footprint= result)

def compare(activity, distance, people=1):
    """ 
    calculate the CO2 emission for each
    compare the values
    take the least value
    print the least vaue
    """ 
    choosen_value =  estimate_carbon_footprint(activity, distance, people)
    least_value = choosen_value
    green_activity = activity
    for key,value in emission_dict.items():
          print("***{}***{}***".format(key,value))
          carbon_footprint =estimate_carbon_footprint(key, distance, people)
          if carbon_footprint < least_value:
              least_value = carbon_footprint
              green_activity = key
    output = "Carbon footprint for {} is {} kg CO2. Most green activity is {}, with carbon footprint {}".format(activity,choosen_value,green_activity,least_value)
    return output



if __name__ == "__main__":
    app.run(debug=True)
