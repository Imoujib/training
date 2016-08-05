from openerp import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'


    instructor = fields.Boolean(string="Instituteur",)

    session_ids = fields.Many2many(comodel_name="openacademy.session", relation="session_partner_rel",
                                   column1="partner_id", column2="session_id", string="Sessions", )