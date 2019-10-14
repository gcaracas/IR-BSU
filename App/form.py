from wtforms import Form, StringField, SelectField

class SearchForm(Form):
    prompt = StringField('Enter Query:')
    search = StringField('')
