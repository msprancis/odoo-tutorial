from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate bids"
    _order = "id desc"
    _sql_constraints = [
        ("expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("selling_price", "CHECK(selling_price >= 0)", "The offer price must be positive"),
    ]
    
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), days=3), string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(string="Status", selection=[('New', 'New'), ('Offer Received', 'Offer Received'), 
                                        ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')],
                                        required=True, copy=False, default='New')
    
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesman_users_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Integer(compute="_compute_best_price", string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
        #     max_price = 0
        #     for offer in record.offer_ids:
        #         if offer.price > max_price:
        #             max_price = offer.price
        #     record.best_price = max_price
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        for record in self:
            if record.state == 'Canceled':
                raise UserError('Canceled property can not be sold')
            record.state = "Sold"
        return True
    def action_cancel(self):
        for record in self:
            if record.state == 'Sold':
                raise UserError('Sold property can not be canceled')
            record.state = "Canceled"
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01) and record.selling_price < record.expected_price * 0.9:
                raise ValidationError("selling price cannot be lower than 90% of the expected price")
        # all records passed the test, don't return anything

    @api.ondelete(at_uninstall=False)
    def _unlink_check(self):
        for r in self:
            if r.state == 'New' or r.state == 'Canceled':
                raise UserError('Can\'t delete New or Canceled')
