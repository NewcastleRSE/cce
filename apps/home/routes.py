# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import Users
from apps.home.models import Entries
from apps import db


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/createEntry', methods=['GET', 'POST'])
@login_required
def createEntry():
    if request.method == 'POST':
        print("update db")
        print(request.form)
        year = request.form['year']
        manufactured = request.form['manufactured']
        acquired = request.form['acquired']
        imported = request.form['imported']
        recycled = request.form['recycled']
        transferred = request.form['transferred']
        exported = request.form['exported']
        untracked = request.form['untracked']
        new_entry = Entries(uesr_id=1, year=year, manufactured=manufactured, acquired=acquired, imported=imported, recycled=recycled, transferred=transferred, exported=exported, untracked=untracked)
        db.session.add(new_entry)
        db.session.commit()
        return redirect('home/forms-enrty.html')

    else:
        render_template('home/forms-entry.html')

    return render_template('home/index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        data = Users.query.all()

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment, data=data)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
