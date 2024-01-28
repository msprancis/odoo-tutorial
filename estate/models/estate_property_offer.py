from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('Accepted', 'Accepted'), ('Refused', 'Refused')], copy=False)
    validity = fields.Integer(default=7, string='Validity (days)')
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.deadline = fields.Date.add(record.create_date if record.create_date else fields.Date.today(), days=record.validity)
    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.deadline - fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()).days

    def action_accept(self):
        if "Accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer has already been accepted.")     
        for record in self:
            record.status = 'Accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_partner_id = record.partner_id
        return True    
    def action_refuse(self):
        for record in self:
            record.status = 'Refused'
        return True