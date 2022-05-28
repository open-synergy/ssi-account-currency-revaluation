# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class AccountMoveLine(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"

    currency_revaluation_id = fields.Many2one(
        string="# Currency Revaluation",
        comodel_name="account.currency_revaluation",
        ondelete="restrict",
        readonly=True,
    )
