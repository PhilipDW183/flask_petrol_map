from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length, Regexp
import re

FUEL_TYPES = [("diesel","Diesel"),
              ("octange_91", "Octane 91"),
              ("octane_95", "Octane 95"),
              ("octane_98", "Octane 98"),
              ("e10", "E10"),
              ("lpg", "LPG"),
               ("LH2", "LH2")]

class PetrolForm(FlaskForm):
    postcode = StringField("Postcode",
                           validators = [DataRequired(),
                                         Length(min=5, max=7,
                                                message="Should be 5 to 7 letters"),
                                        Regexp(regex=r'\b[A-Z]{1,2}[0-9][A-Z0-9]? [0-9][ABD-HJLNP-UW-Z]{2}\b',
                                               flags=re.IGNORECASE,
                                               message="Not a recognised postcode")] )
    fuel_type = SelectField("Fuel Type",
                            choices = FUEL_TYPES,
                            validators = [DataRequired()])
    
