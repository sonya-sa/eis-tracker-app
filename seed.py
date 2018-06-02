"""Utility file to seed EIS database from EPA data seed_data/"""

import datetime
from sqlalchemy import func

from model import connect_to_db, db, EIS_data, State, Project_State
from server import app

def load_EIS_data(epa_scrape_all_info):
    """Load projects from open_comment.csv into database."""

    print "EIS Data"

    for row in open(epa_scrape_all_info):
        if row[0] == "E":
            continue
        row = row.rstrip()

        #unpack info; row.split(",")
        eis_id, title, title_link, document, comment_letter_date_str, \
        federal_register_date, comment_due_date_str, agency, state, \
        download_documents, download_link, contact_name, contact_phone = row.split(",")

        #for each state in states column, create object (project-state; eis_id=state_id); do in third function

        #ensure strings are stored as datetime objects in database
        if comment_letter_date_str:
            epa_comment_letter_date = datetime.datetime.strptime(comment_letter_date_str, "%m/%d/%y")
        else:
            epa_comment_letter_date = None

        if comment_due_date_str:
            comment_due_date = datetime.datetime.strptime(comment_due_date_str, "%m/%d/%y")
        else:
            comment_due_date = None

        projects = EIS_data(eis_id=eis_id, title=title, title_link=title_link,
                            document=document, epa_comment_letter_date=epa_comment_letter_date,
                            federal_register_date=federal_register_date, comment_due_date=comment_due_date,
                            agency=agency, download_link=download_link)

        #Add to the session to store info
        db.session.add(projects)

    #Once done, commit work
    db.session.commit()

def load_States(states_coordinates):
    """Load states from state_coordinates.csv into database."""

    print "State Coordinates"

    #parsing csv:
    for row in open(states_coordinates):
        row = row.rstrip()

        #unpack info; row.split(",")
        state_id, geo_lat, geo_long = row.split(",")
        print geo_lat
        print geo_long

        geo_lat = float(geo_lat)
        geo_long = float(geo_long)


        states = State(state_id=state_id, geo_lat=geo_lat, geo_long=geo_long)

        #add to the session to store info
        db.session.add(states)

    #commit to db and close
    db.session.commit()


def load_Project_States(states_coordinates):

    print "Project States"

    for row in open(epa_scrape_all_info):
        if row[0] == "E":
            continue
        row = row.rstrip()

        #unpack info; row.split(",")
        eis_id, title, title_link, document, comment_letter_date_str,\
        federal_register_date, comment_due_date_str, agency, state_col, \
        download_documents, download_link, contact_name, contact_phone = row.split(",")

        state_col = state_col.split(' - ')

        for state in state_col:

            #state_id is column name, state is variable within function
            project_states = Project_State(state_id=state, eis_id=eis_id) 

            db.session.add(project_states)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    epa_scrape_all_info = "epa_scrape_all_info.csv"
    states_coordinates = "state_coordinates.csv"
    load_EIS_data(epa_scrape_all_info)
    load_States(states_coordinates)
    load_Project_States(states_coordinates)
