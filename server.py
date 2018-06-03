import datetime
from jinja2 import StrictUndefined
from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, EIS_data, State, Project_State

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# If you use an undefined variable in Jinja2, it fails silently.
# Now, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/states_with_projects.json')
def all_state_with_projects():

    #State table has relationship to EIS_data table
    #returns all projects with their EIS_data and State info(geo_lat/geo_long/state_id)
    # __repr__ displays project title and state
    states = State.query.all()
    print states

    #returns all projects in states with projects
    # prints ([state, projects_in_state])
    states_with_projects = {}



    #iterates through all projects starting from index 1
    #index 0 of dataset (epa_scrape_all_info) shows column titles; thus, we skip
    for state in states:


        states_with_projects[state.state_id] ={
            'geo_lat': state.geo_lat,
            'geo_long': state.geo_long,
            'projects': []
        }

        # query for all projects in this state
        # relationship between Project_State table and EIS_data allows access to project info
        # e.g return: [<Project States project_state_id= 13 state_id=CA>, <Project States project_state_id= 18 state_id=CA>, <Project States project_state_id= 28 state_id=CA>]
        #<Project title=Mather Specific Plan Project state=[<State state_id=CA>]>
        #<type 'datetime.datetime'>
        #<Project title=Nevada and Northeastern California Greater Sage-Grouse Draft Resource Management Plan Amendment and Environmental Impact Statement state=[<State state_id=CA>, <State state_id=NV>]>
        #<type 'datetime.datetime'>
        #<Project title=Pure Water San Diego Program North City Project state=[<State state_id=CA>]>
        #<type 'datetime.datetime'>

        state_project_relationships = Project_State.query.filter_by(state_id=state.state_id).all()
        print state_project_relationships


        #if state has projects, enter for loop
        if len(state_project_relationships) > 0:

            #returns all projects in state
            #e.g. [<Project title=Southern Gardens Citrus Nursery LLC Permit to Release Genetically Engineered Citrus tristeza virus Draft Environmental Impact Statement state=[<State state_id=NAT>]>]
            #projects_in_state = []

            #for each project in state, access EIS_data table by relationship
            #relationship: project_state_id = state_id
            #e.g. <Project States project_state_id= 24 state_id=AK>
            for relationship in state_project_relationships:

                #query our EIS_data by eis_id and grab all info related to that project
                #place project details into list

                eis_datas = EIS_data.query.filter_by(eis_id=relationship.eis_id).all()
                states_with_projects[state.state_id]['projects'] += [{
                    'eis id': project.eis_id, 
                    'title': project.title, 
                    'title link': project.title_link,
                    'document': project.document,
                    'EPA comment letter date': project.epa_comment_letter_date,
                    'federal reigster date': project.federal_register_date,
                    'Comment due date': project.comment_due_date,
                    'download documents link': project.download_documents,
                    'download link': project.download_link,
                    'contact name': project.contact_name,
                    'contact phone': project.contact_phone


                } for project in eis_datas]


                #states_with_projects[state.]


            # states_with_projects.append([state, projects_in_state])

    # state_dict = {'data' : states_with_projects}
    #test_dict = str(states_with_projects)


    return jsonify(states_with_projects)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')

    print "connect"
