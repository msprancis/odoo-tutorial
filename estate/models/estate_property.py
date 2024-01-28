from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Real Estate bids"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), days=3))
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
    state = fields.Selection(selection=[('New', 'New'), ('Offer', 'Offer'), ('Received', 'Received'), 
                                        ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Canceled', 'Canceled')],
                                        required=True, copy=False, default='New')
    
    type = fields.Many2one("estate.property.type", string="Property Type")
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
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''
