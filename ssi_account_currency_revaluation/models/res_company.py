# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = "res.company"

    unrealized_gain_account_id = fields.Many2one(
        string="Unrealized Gain Account",
        comodel_name="account.account",
        ondelete="restrict",
    )
    unrealized_loss_account_id = fields.Many2one(
        string="Unrealized Loss Account",
        comodel_name="account.account",
        ondelete="restrict",
    )
    unrealized_journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "general"),
        ],
        ondelete="restrict",
    )
