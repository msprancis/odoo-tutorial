from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"
    _order = "sequence"
    _sql_constraints = [('name', 'unique(name)', 'Name must be unique!')]

    name = fields.Char(required=True)
    sequence = fields.Integer()
    offer_count = fields.Integer(compute="_compute_offer_count")
    property_ids = fields.One2many("estate.property", "type_id")
    offer_ids = fields.One2many("estate.property.offer", "type_id")

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # we need this function only if button in estate_property_type_view is defined as this:
    # <!-- <button name="action_view_offers" type="object" class="oe_stat_button" icon="fa-money">  estate_property_offer_action -->
    # def action_view_offers(self):
    #     res = self.env.ref("estate.estate_property_offer_action").read()[0]
    #     return res