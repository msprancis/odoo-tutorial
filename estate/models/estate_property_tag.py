from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name"
    _sql_constraints = [('name', 'unique(name)', 'Name must be unique!')]

    name = fields.Char(required=True)
    color = fields.Integer("Color Index")
