# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.authentication.models import Users
from apps.home.models import Entries, Transfers
from apps import db


@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/createEntry', methods=['GET', 'POST'])
@login_required
def createEntry():
    if request.method == 'POST':
        print(request.form)
        year = int(request.form['year'])
        manufactured = int(request.form['manufactured'])
        acquired = int(request.form['acquired'])
        imported = int(request.form['imported'])
        recycled = int(request.form['recycled'])
        transferred = int(request.form['transferred'])
        exported = int(request.form['exported'])
        untracked = manufactured + acquired + imported - recycled - transferred - exported
        new_entry = Entries(user_id=1, year=year, manufactured=manufactured, acquired=acquired, imported=imported, recycled=recycled, transferred=transferred, exported=exported, untracked=untracked)
        try:
            db.session.add(new_entry)
            db.session.commit()
            return redirect('/index')
        except:
            return "There was an issue adding your entry"

    else:
        render_template('home/forms-entry.html')

    return render_template('home/index.html', segment='index')

@blueprint.route('/createTransfer', methods=['GET', 'POST'])
@login_required
def createTransfer():
    if request.method == 'POST':
        print(request.form)
        year = int(request.form['year'])
        from_user = request.form['from_user']
        to_user = request.form['to_user']
        olefin_mass = int(request.form['olefin_mass'])
        new_transfer = Transfers(user_id=1, year=year, from_user=from_user, to_user=to_user, olefin_mass=olefin_mass)
        try:
            db.session.add(new_transfer)
            db.session.commit()
            return redirect('/index')
        except:
            return "There was an issue adding your transfer"

    else:
        render_template('forms-transfer.html')

    return render_template('home/index.html', segment='index')

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        users = Users.query.all()
        entries = Entries.query.all()
        transfers = Transfers.query.all()

        # Serve the file (if exists) from app/templates/home/FILE.html
        if template.endswith('tables-users.html'):
            return render_template("home/" + template, segment=segment, data=users)
        elif template.endswith('tables-entries.html'):
            return render_template("home/" + template, segment=segment, data=entries)
        elif template.endswith('tables-transfers.html'):
            return render_template("home/" + template, segment=segment, data=transfers)
        else:
            return render_template("home/" + template, segment=segment)

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
