from wtforms import Form, BooleanField, TextField, PasswordField, validators

class NewMenuItemForm(Form):
	new_menu_item = TextField('New Menu Item')
	item_description =  TextField('Description')
	item_price = TextField('Price')	

