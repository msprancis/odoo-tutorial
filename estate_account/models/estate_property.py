from odoo import fields, models

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # self.env['account.move'].create(values)
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        # Another way to get the journal:
        # journal = self.env["account.move"].with_context(default_move_type="out_invoice")._get_default_journal()
        for prop in self:
            self.env["account.move"].create({
                "partner_id": prop.buyer_partner_id.id,
                "move_type": "out_invoice",
                "journal_id": journal.id,
                "line_ids": [
                    fields.Command.create({
                        "name": prop.name,
                        "quantity": 1,
                        "price_unit": prop.selling_price * 0.06,
                    }),
                    fields.Command.create({
                        "name": "Admin fee",
                        "quantity": 1,
                        "price_unit": 100,
                    })
                ]
            })
        return super().action_sold()
    