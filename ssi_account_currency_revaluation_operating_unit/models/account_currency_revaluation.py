# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountCurrencyRevaluation(models.Model):
    _name = "account.currency_revaluation"
    _inherit = [
        "account.currency_revaluation",
        "mixin.single_operating_unit",
    ]
