# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _name = "res.config.settings"
    _inherit = [
        "res.config.settings",
        "abstract.config.settings",
    ]

    unrealized_gain_account_id = fields.Many2one(
        string="Unrealized Gain Account",
        comodel_name="account.account",
        related="company_id.unrealized_gain_account_id",
        readonly=False,
    )
    unrealized_loss_account_id = fields.Many2one(
        string="Unrealized Loss Account",
        comodel_name="account.account",
        related="company_id.unrealized_loss_account_id",
        readonly=False,
    )
    unrealized_journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[
            ("type", "=", "general"),
        ],
        related="company_id.unrealized_journal_id",
        readonly=False,
    )

    module_ssi_account_currency_revaluation_related_attachment = fields.Boolean(
        "Currency Revaluation - Related Attachment",
    )
    module_ssi_account_currency_revaluation_custom_information = fields.Boolean(
        "Currency Revaluation - Custom Information",
    )
    module_ssi_account_currency_revaluation_status_check = fields.Boolean(
        "Currency Revaluation - Status Check",
    )
    module_ssi_account_currency_revaluation_state_change_constrains = fields.Boolean(
        "Currency Revaluation - State Change Constrains",
    )
    module_ssi_account_currency_revaluation_qrcode = fields.Boolean(
        "Currency Revaluation - QR Code",
    )
